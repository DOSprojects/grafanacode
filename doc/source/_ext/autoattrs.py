#******************************************************************************
# autoattrs.py
#
# document attrs library attributes
#
#  V0.9 LDO 19/10/2022: initial version
#
# see: https://github.com/domdfcoding/attr_utils
# see: https://github.com/domdfcoding/domdf_python_tools
#
#******************************************************************************

#******************************************************************************
# EXTERNAL MODULE REFERENCES
#******************************************************************************
import warnings
import attr
import attrs
from textwrap             import dedent
from typing               import Any, Dict, List, MutableMapping, Optional, Pattern, Tuple, Type, TypeVar
from typing_extensions    import Protocol, runtime_checkable
from sphinx.application   import Sphinx  # nodep
from sphinx.ext.autodoc   import ClassDocumenter, Documenter  # nodep
from sphinx.pycode        import ModuleAnalyzer  # nodep
from sphinx_toolbox       import __version__  # nodep
from sphinx_toolbox.utils import Param, SphinxExtMetadata, flag, parse_parameters, unknown_module_warning  # nodep
from sphinx_toolbox.more_autosummary import PatchedAutoSummClassDocumenter  # nodep

#******************************************************************************
# __all__
#******************************************************************************
__all__ = ["AttrsDocumenter", "setup"]

#******************************************************************************
# CLASSES
#******************************************************************************
class AttrsClass(Protocol):
    """
    :class:`~typing.Protocol` for attrs classes.
    """
    #: Special attribute used internally by attrs.
    __attrs_attrs__: Tuple[attrs.Attribute, ...]
    __name__: str

#******************************************************************************
class AttrsDocumenter(PatchedAutoSummClassDocumenter):
    """
    :class: extension of Sphinx Autodoc functionality
    """
    objtype = "attrs"
    directivetype = "class"
    priority = ClassDocumenter.priority + 1
    option_spec = {
            **PatchedAutoSummClassDocumenter.option_spec,
            "no-init-attribs": flag,
            }
    object: Type[AttrsClass]

    #**********************************************************
    @classmethod
    def can_document_member(cls, member: Any, membername: str, isattr: bool, parent: Any) -> bool:
        """
        Check if a member can be documented by this documenter.
        """
        return attrs.has(member) and isinstance(member, type)

    #**********************************************************
    def add_content(self, more_content: Any, no_docstring: bool = False) -> None:  # type: ignore
        """
        Add extra content (from docstrings, attribute docs etc.), but not the class docstring.

        :param more_content:
        :param no_docstring:
        """
        sourcename = self.get_sourcename()
        params, pre_output, post_output = self._get_docstring()
        self.add_line('', sourcename)
        for line in list(self.process_doc([pre_output])):
            self.add_line(line, sourcename)
        self.add_line('', sourcename)

    #**********************************************************
    def _get_docstring(self) -> Tuple[Dict[str, Param], List[str], List[str]]:
        """
        Return params, pre_output, post_output.
        """

        tab_size = self.env.app.config.docutils_tab_width # Size varies depending on docutils config
        if self.object.__doc__:
            docstring = dedent(self.object.__doc__).expandtabs(tab_size).split('\n')
        else:
            docstring = []
        return parse_parameters(docstring, tab_size=tab_size)

    #**********************************************************
    def import_object(self, raiseerror: bool = False) -> bool:
        """
        Import the object given by ``self.modname`` and ``self.objpath`` and set it as ``self.object``.

        :param raiseerror:
        :return: :py:obj:`True` if successful, :py:obj:`False` if an error occurred.
        """

        ret = super().import_object(raiseerror)
        return ret

    #**********************************************************
    def _resolve_validators(self, validator, doc, prepend):
        #print('TP : ', type(validator), dir(validator))
        if type(validator) is attr.validators._InstanceOfValidator:
            #print('0', validator.type)
            valtype = str(validator.type).split("'")[1::2][0]
            if prepend == '':
                doc.append(prepend + f'**type:** {valtype}')
            else:
                doc.append(prepend + f' {valtype}')
        elif type(validator) is attr.validators._InValidator:
            #print('1', self.get_sourcename())
            doc.append(prepend + f'**in:** {validator.options}')
        elif type(validator) is attr.validators._DeepIterable:
            #print('2', self.get_sourcename())
            #doc.append(prepend + f'**deep iteratable:** ')
            self._resolve_validators(validator.iterable_validator, doc, f'**type:** ')
            self._resolve_validators(validator.member_validator, doc, f'**of:** ')
        elif type(validator) is attr.validators._OptionalValidator:
            #print('3', self.get_sourcename())
            doc.append(prepend + f'**optional** ')
            #print('d ', dir(validator))
            self._resolve_validators(validator.validator, doc, '')
        else:
            #print('4', self.get_sourcename())
            doc.append(prepend + f'**validator:** {str(validator)}')


    #**********************************************************
    def _add_attributes(self):
        # mapping of member names to docstrings (as list of strings)
        member_docstrings = {}
        for k, v in ModuleAnalyzer.for_module(self.object.__module__).find_attr_docs().items():
            member_docstrings[k[1]] = v
        # set sourcename and add content from attribute documentation
        sourcename = self.get_sourcename()
        parameter_docs = []
        params, pre_output, post_output = self._get_docstring()
        all_docs = {}
        for attribute in attrs.fields(self.object):
            #print("Attrib: ", a)
            field = attribute.name
            doc = []
            # Prefer doc from class docstring
            if field in params:
                doc, arg_type = params.pop(field).values()  # type: ignore
            # Otherwise use attribute docstring
            if not ''.join(doc).strip() and field in member_docstrings:
                doc = member_docstrings[field]
            if attribute.init==False:
                doc.append(f'**read only** ')
            if attribute.default is None:
                doc.append(f'**default:** None')
            elif attribute.default:
                doc.append(f'**default:** {str(attribute.default)}')
            if attribute.validator:
                self._resolve_validators(attribute.validator, doc, '')
            field_entry = [f":param {field}:", *doc]
            parameter_docs.append('* ' + ' - '.join(field_entry))
            all_docs[field] = ' '.join(doc)  #.strip()
        self.add_line('', sourcename)
        for line in list(self.process_doc([[*parameter_docs, '', '', *post_output]])):
            self.add_line(line, sourcename)
            #print('addedlines: ', line)
        self.add_line('', sourcename)

    #**********************************************************
    def sort_members(self, documenters: List[Tuple[Documenter, bool]], order: str) -> List[Tuple[Documenter, bool]]:
        """
        Sort the given member list and add attribute docstrings to the class docstring.

        :param documenters:
        :param order:
        """

        # The documenters for the fields and methods, in the desired order
        # The fields will be in bysource order regardless of the order option
        documenters = super().sort_members(documenters, order)
        #process only once
        if hasattr(self, "_docstring_processed"):
            return documenters
        self._add_attributes()
        self._docstring_processed = True
        if hasattr(self.object, "__slots__"):
            slots_dict: MutableMapping[str, Optional[str]] = {}
            for item in self.object.__slots__:
                if item in all_docs:
                    slots_dict[item] = all_docs[item]
                else:
                    slots_dict[item] = None
            self.object.__slots__ = slots_dict
        if hasattr(self, "add_autosummary"):
            self.add_autosummary()
        return documenters

    #**********************************************************
    def filter_members(self, members: List[Tuple[str, Any]], want_all: bool) -> List[Tuple[str, Any, bool]]:
        """
        Filter the list of members to always include init attributes unless the    ``:no-init-attribs:`` flag was given.

        :param members:
        :param want_all:
        """

        def unskip_attrs(app, what, name, obj, skip, options):
            if skip and not no_init_attribs:
                return not (name in attrib_names)
            elif no_init_attribs and (name in attrib_names):
                return True
            return None

        attrib_names = (attribute.name for attribute in attrs.fields(self.object) if attribute.init)
        #print("PNAMES: ", attrib_names)
        no_init_attribs = self.options.get("no-init-attribs", False)
        listener_id = self.env.app.connect("autodoc-skip-member", unskip_attrs)
        members_ = super().filter_members(members, want_all)
        self.env.app.disconnect(listener_id)
        return members_

    #**********************************************************
    def generate(self, more_content: Optional[Any]=None, real_modname: Optional[str]=None, check_module: bool=False, all_members: bool=False) -> None:
        """
        Generate reST for the object given by ``self.name``, and possibly for its members.

        :param more_content: Additional content to include in the reST output.
        :param real_modname: Module name to use to find attribute documentation.
        :param check_module: If :py:obj:`True`, only generate if the object is defined in the module name it is imported from.
        :param all_members: If :py:obj:`True`, document all members.
        """

        if not self.parse_name():           # pragma: no cover
            unknown_module_warning(self)    # need a module to import
            return None
        if not self.import_object():        # now, import the module and get object to document
            return None                     # pragma: no cover
        return super().generate(
                more_content=more_content,
                real_modname=real_modname,
                check_module=check_module,
                all_members=all_members,
                )

#******************************************************************************
# SPHINX SETUP
#******************************************************************************
def setup(app: Sphinx) -> SphinxExtMetadata:
    """
    Setup :mod:`autoattrs`.

    :param app:
    """

    # hack to get the docutils tab size, as there doesn't appear to be any other way
    app.setup_extension("sphinx_toolbox.tweaks.tabsize")
    app.setup_extension("sphinx_toolbox.more_autosummary")
    app.add_autodocumenter(AttrsDocumenter)
    return {"version": __version__, "parallel_read_safe": True}
