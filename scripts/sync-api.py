#!/usr/bin/env python3
"""Generate a source-level Spring controller index. Does not infer OpenAPI schemas."""
import argparse
import itertools
import json
import re
import subprocess
from pathlib import Path

MAPPING = re.compile(r'@(?:[\w]+\.)*(Get|Post|Put|Delete|Patch|Request)Mapping\b')
STRING = re.compile(r'"(?:\\.|[^"\\])*"')


def mask_java(text, strings=False):
    """Keep offsets/newlines while masking comments, and optionally string literals."""
    chars = list(text)
    i = 0
    while i < len(text):
        end = None
        if text.startswith('//', i):
            end = text.find('\n', i)
            end = len(text) if end < 0 else end
        elif text.startswith('/*', i):
            pos = text.find('*/', i + 2)
            end = len(text) if pos < 0 else pos + 2
        elif text[i] in ['"', "'"]:
            quote = text[i]
            pos = i + 1
            while pos < len(text):
                if text[pos] == '\\':
                    pos += 2
                    continue
                if text[pos] == quote:
                    pos += 1
                    break
                pos += 1
            if not strings:
                i = pos
                continue
            end = pos
        if end is not None:
            for n in range(i, end):
                if chars[n] != '\n':
                    chars[n] = ' '
            i = end
        else:
            i += 1
    return ''.join(chars)


def arguments(text, start):
    while start < len(text) and text[start].isspace():
        start += 1
    if start >= len(text) or text[start] != '(':
        return '', start
    masked = mask_java(text, strings=True)
    level = 0
    for end in range(start, len(text)):
        if masked[end] == '(':
            level += 1
        elif masked[end] == ')':
            level -= 1
            if level == 0:
                return text[start + 1:end], end + 1
    raise ValueError('Unclosed annotation arguments')


def split_arguments(args):
    masked = mask_java(args, strings=True)
    depth = 0
    begin = 0
    result = []
    for i, char in enumerate(masked):
        if char in '({[':
            depth += 1
        elif char in ')}]':
            depth -= 1
        elif char == ',' and depth == 0:
            result.append(args[begin:i].strip())
            begin = i + 1
    result.append(args[begin:].strip())
    return result


def paths_from(args):
    expression = None
    for i, part in enumerate(split_arguments(args)):
        named = re.match(r'^(value|path)\s*=\s*([\s\S]+)$', part)
        if named:
            expression = named.group(2)
            break
        if i == 0 and part.startswith(('"', '{')):
            expression = part
            break
        if i == 0 and part and '=' not in part:
            raise ValueError('Non-literal mapping path requires an explicit parser rule: ' + part)
    if expression is None:
        return ['']
    rest = STRING.sub('', expression)
    if re.sub(r'[\s{},]', '', rest):
        raise ValueError('Non-literal mapping path requires an explicit parser rule: ' + expression)
    paths = [json.loads(m.group()) for m in STRING.finditer(expression)]
    return paths or ['']


def verbs_from(kind, args):
    if kind != 'Request':
        return [kind.upper()]
    return sorted(set(re.findall(r'RequestMethod\.(\w+)', args))) or ['ANY']


def join_path(*parts):
    return '/' + '/'.join(part.strip('/') for part in parts if part.strip('/'))


def controller_condition(prefix):
    match = re.search(r'@(?:[\w]+\.)*ConditionalOnProperty\b', prefix)
    if not match:
        return '按其他条件装配，见源码' if re.search(r'@(?:[\w]+\.)*Conditional', prefix) else ''
    args, _ = arguments(prefix, match.end())
    def value(name, fallback=''):
        found = re.search(r'\b' + name + r'\s*=\s*("(?:\\.|[^"\\])*")', args)
        return json.loads(found.group(1)) if found else fallback
    name = value('name') or value('value')
    prop = '.'.join(x for x in [value('prefix'), name] if x)
    return prop + '=' + value('havingValue', '非 false') if prop else '按属性条件装配，见源码'


def parse_controller(source, context=''):
    clean = mask_java(source)
    masked = mask_java(source, strings=True)
    declaration = re.search(r'\bclass\s+(\w+)', masked)
    if not declaration:
        return []
    prefix = clean[:declaration.start()]
    if not re.search(r'@(?:[\w]+\.)*(?:RestController|Controller)\b', prefix):
        return []
    body = masked.find('{', declaration.end())
    if body < 0:
        return []
    depths = []
    depth = 0
    for char in masked:
        depths.append(depth)
        depth += (char == '{') - (char == '}')
    class_mappings = [m for m in MAPPING.finditer(clean[:declaration.start()]) if masked[m.start()] == '@']
    base_paths, class_verbs = [''], ['ANY']
    if class_mappings:
        mapping = class_mappings[-1]
        args, _ = arguments(clean, mapping.end())
        base_paths = paths_from(args)
        class_verbs = verbs_from(mapping.group(1), args)
    condition = controller_condition(prefix)
    rows = []
    for mapping in MAPPING.finditer(clean, body + 1):
        if masked[mapping.start()] != '@' or depths[mapping.start()] != 1:
            continue
        args, end = arguments(clean, mapping.end())
        signature = re.search(r'\b(?:public|protected|private)\b[^;{}]*?\b(\w+)\s*\(', masked[end:])
        if not signature:
            raise ValueError('Cannot identify method after mapping in ' + declaration.group(1))
        verbs = verbs_from(mapping.group(1), args)
        if class_verbs != ['ANY']:
            verbs = class_verbs if verbs == ['ANY'] else sorted(set(verbs) & set(class_verbs))
        for base, path, verb in itertools.product(base_paths, paths_from(args), verbs):
            rows.append({'controller': declaration.group(1), 'handler': signature.group(1),
                         'httpMethod': verb, 'path': join_path(context, base, path),
                         'condition': condition, 'line': clean.count('\n', 0, mapping.start()) + 1})
    return rows


def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args], text=True).strip()


def generate(root, repos_root):
    configs = json.loads((root / 'scripts/api-sources.json').read_text())
    sources, all_rows = [], []
    for config in configs:
        repo = repos_root / config['repo']
        java = repo / config['module'] / 'src/main/java'
        if not java.is_dir():
            raise ValueError('Source directory missing: ' + str(java))
        revision = git(repo, 'rev-parse', 'HEAD')
        dirty = bool(git(repo, 'status', '--porcelain', '--', config['module'] + '/src/main/java'))
        rows = []
        for path in sorted(java.rglob('*.java')):
            try:
                parsed = parse_controller(path.read_text(), config['context'])
            except ValueError as e:
                raise ValueError(str(path.relative_to(repo)) + ': ' + str(e)) from e
            for row in parsed:
                row['source'] = f"{config['remote']}/blob/{revision}/{path.relative_to(repo).as_posix()}#L{row['line']}"
                row['service'] = config['service']
                rows.append(row)
        rows.sort(key=lambda x: (x['controller'], x['path'], x['httpMethod'], x['handler']))
        if not rows:
            raise ValueError('No mapped controllers found for ' + config['service'])
        sources.append({'service': config['service'], 'repository': config['remote'], 'revision': revision,
                        'localChanges': dirty, 'endpointCount': len(rows)})
        all_rows.extend(rows)
        lines = ["---", "editLink: false", "---", "", f"# {config['title']}", '', '> 本页由 `npm run api:sync` 生成，请勿手动修改。', '',
                 f"- 服务注册名：`{config['service']}`", f"- 源码：[{config['repo']} · {revision[:7]}]({config['remote']}/tree/{revision})",
                 f"- servlet context-path：`{config['context'] or '/'}`", f"- 路径组合数：{len(rows)}", '',
                 '路径已包含服务 context-path，不包含环境域名及入口代理前缀。它是源码索引，不代表功能已启用或已部署，详见 [覆盖范围](/api/)。', '']
        if dirty:
            lines.extend(['::: warning 本地源码快照', '源码包含未提交变更；索引反映本地文件，链接指向上述 HEAD，可能存在差异。', ':::', ''])
        for controller, entries in itertools.groupby(rows, lambda x: x['controller']):
            entries = list(entries)
            lines += ['## ' + controller, '']
            if entries[0]['condition']:
                lines += ['启用条件：`' + entries[0]['condition'] + '`。', '']
            if controller == 'LegacyDocumentController':
                lines += ['兼容入口返回 **410 Gone**，请迁移到文档接口。', '']
            lines += ['| HTTP | 服务 HTTP 路径 | 控制器方法 |', '| --- | --- | --- |']
            for entry in entries:
                lines.append(f"| `{entry['httpMethod']}` | `{entry['path']}` | [{entry['handler']}]({entry['source']}) |")
            lines.append('')
        (root / 'docs/api/generated' / (config['id'] + '.md')).write_text('\n'.join(lines))
        print(config['service'] + ': ' + str(len(rows)) + ' path combinations')
    output = {'schemaVersion': 1, 'kind': 'spring-controller-source-index', 'sources': sources, 'endpoints': all_rows}
    (root / 'docs/public/api-index.json').write_text(json.dumps(output, ensure_ascii=False, indent=2) + '\n')


def main():
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repos-root', type=Path, default=root.parent, help='Parent of the three source repositories')
    args = parser.parse_args()
    generate(root, args.repos_root.resolve())


if __name__ == '__main__':
    main()
