import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location('sync_api', Path(__file__).resolve().parents[1] / 'scripts/sync-api.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
parse = module.parse_controller


class ControllerIndexTest(unittest.TestCase):
    def test_context_and_named_http_method(self):
        source = '''
@RestController
@RequestMapping("api/v1/target/")
public class TargetController {
 @RequestMapping(value="get", method=RequestMethod.GET)
 public String get(@RequestParam String id) { return "ok"; }
}'''
        self.assertEqual([(r['httpMethod'], r['path'], r['handler']) for r in parse(source, '/target-service')],
                         [('GET', '/target-service/api/v1/target/get', 'get')])

    def test_arrays_any_and_retired_paths(self):
        source = '''
@RestController @RequestMapping({"/basis", "/case", "/post"})
public class LegacyDocumentController {
 @RequestMapping({"", "/**"}) public Object retired() { return null; }
}'''
        rows = parse(source, '/community')
        self.assertEqual(len(rows), 6)
        self.assertEqual({r['httpMethod'] for r in rows}, {'ANY'})
        self.assertIn('/community/post/**', {r['path'] for r in rows})

    def test_comments_literals_nested_classes_and_path_braces(self):
        source = '''
// @RestController public class Fake {}
@RestController @RequestMapping("/channel/{channelId}")
public class RealController {
 String x = "@GetMapping(\"/fake\") public String fake() {";
 /* @DeleteMapping("/fake") public void fake() {} */
 @GetMapping("/messages") public java.util.List<String> messages() { return null; }
 public class Nested { @PostMapping("/ignore") public void ignored() {} }
}'''
        rows = parse(source)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]['path'], '/channel/{channelId}/messages')
        self.assertEqual(rows[0]['handler'], 'messages')

    def test_condition_and_path_attribute(self):
        source = '''
@RestController
@ConditionalOnProperty(prefix="alisa.authorization", name="enabled", havingValue="true")
public class AuthController {
 @PostMapping(path="/check", produces="application/json") public Object check() { return null; }
}'''
        row = parse(source)[0]
        self.assertEqual(row['condition'], 'alisa.authorization.enabled=true')
        self.assertEqual(row['path'], '/check')

    def test_nonliteral_paths_fail_instead_of_silently_omitting(self):
        source = '@RestController @RequestMapping(API_PREFIX) public class C { @GetMapping("/get") public void get() {} }'
        with self.assertRaisesRegex(ValueError, 'Non-literal'):
            parse(source)

    def test_non_controller_and_class_method_constraint(self):
        self.assertEqual(parse('public class C { @GetMapping("/get") public void get() {} }'), [])
        rows = parse('@RestController @RequestMapping(value="/api", method=RequestMethod.POST) public class C { @RequestMapping("/save") public void save() {} }')
        self.assertEqual(rows[0]['httpMethod'], 'POST')


if __name__ == '__main__':
    unittest.main()
