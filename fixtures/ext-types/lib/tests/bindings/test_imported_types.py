# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/. */

import unittest
import urllib
from imported_types_lib import *
from imported_types_sublib import *
from uniffi_one_ns import *
from ext_types_custom import *

def test_external_callback_interface_impl():
    """
    Implement a trait from an external crate in Python and pass it to a function from this
    crate.  This tests #2343 -- the codegen for this module needs to initialize the vtable from
    uniffi_one.

    This is written as a plain function rather than a unittest, because it
    needs to run first before there's any chance of a `uniffi_one` funciton
    being called.
    """
    class PyUniffiOneImpl(UniffiOneTrait):
        def hello(self):
            return "Hello from Python"
    assert(invoke_uniffi_one_trait(PyUniffiOneImpl()) == "Hello from Python")

class TestIt(unittest.TestCase):
    def test_it(self):
        ct = get_combined_type(None)
        self.assertEqual(ct.uot.sval, "hello")
        self.assertEqual(ct.guid, "a-guid")
        self.assertEqual(ct.url.scheme, 'http')
        self.assertEqual(ct.url.netloc, 'example.com')
        self.assertEqual(ct.url.path, '/')

        ct2 = get_combined_type(ct)
        self.assertEqual(ct, ct2)

        t = get_trait_impl()
        self.assertEqual(t.hello(), "sub-lib trait impl says hello")
        sub = SubLibType(maybe_enum = None, maybe_trait = t, maybe_interface = None)
        self.assertTrue(get_sub_type(sub).maybe_trait is not None)

        ot = ObjectsType(maybe_trait = t, maybe_interface = None, sub = sub)
        self.assertTrue(ot.maybe_trait is not None)
        self.assertEqual(ot.maybe_interface, None)
        self.assertEqual(get_uniffi_one_trait(None), None)

        get_sub_type(sub)

    def test_get_url(self):
        url = urllib.parse.urlparse("http://example.com/")
        self.assertEqual(get_url(url), url)
        self.assertEqual(get_urls([url]), [url])
        self.assertEqual(get_maybe_url(url), url)
        self.assertEqual(get_maybe_url(None), None)
        self.assertEqual(get_maybe_urls([url, None]), [url, None])

    def test_custom_types(self):
        self.assertEqual(get_guid("guid"), "guid")
        self.assertEqual(get_ouid("ouid"), "ouid")
        self.assertEqual(get_ouid("uuid"), "uuid")
        self.assertEqual(get_nested_guid("uuid"), "uuid")
        self.assertEqual(get_imported_handle_u8(None), 3)

    def test_get_uniffi_one_type(self):
        t1 = UniffiOneType(sval="hello")
        self.assertEqual(t1, get_uniffi_one_type(t1))
        self.assertEqual(t1, get_maybe_uniffi_one_type(t1))
        self.assertEqual(None, get_maybe_uniffi_one_type(None))
        self.assertEqual([t1], get_uniffi_one_types([t1]))
        self.assertEqual([t1, None], get_maybe_uniffi_one_types([t1, None]))

    def test_get_uniffi_one_enum(self):
        e = UniffiOneEnum.ONE
        self.assertEqual(e, get_uniffi_one_enum(e))
        self.assertEqual(e, get_maybe_uniffi_one_enum(e))
        self.assertEqual(None, get_maybe_uniffi_one_enum(None))
        self.assertEqual([e], get_uniffi_one_enums([e]))
        self.assertEqual([e, None], get_maybe_uniffi_one_enums([e, None]))

    def test_external_crate_types(self):
        ct = get_combined_type(None)
        self.assertEqual(ct.ecd.sval, "ecd");
        self.assertEqual(get_external_crate_interface("foo").value(), "foo")

    def test_procmacro_types(self):
        t1 = UniffiOneProcMacroType(sval="hello")
        self.assertEqual(t1, get_uniffi_one_proc_macro_type(t1))
        self.assertEqual(t1, get_my_proc_macro_type(t1))

    def test_misc_external_types(self):
        # various edge-cases for various external/custom types.
        self.assertEqual(get_imported_guid("guid"), "guid")
        self.assertEqual(get_imported_ouid("ouid"), "ouid")
        self.assertEqual(get_imported_nested_guid(None), "nested")
        self.assertEqual(get_imported_nested_ouid(None), "nested")
        self.assertEqual(get_nested_external_guid(None), "nested-external")
        self.assertEqual(get_nested_external_ouid(None), "nested-external-ouid")

    def test_external_errors(self):
        with self.assertRaises(UniffiOneError) as cm:
            throw_uniffi_one_error()

        with self.assertRaises(UniffiOneErrorInterface) as cm:
            throw_uniffi_one_error_interface()

if __name__=='__main__':
    test_external_callback_interface_impl()
    unittest.main()
