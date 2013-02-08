import sublime
import sublime_plugin
import re

try:
    from misaka import Markdown, HtmlRenderer, EXT_FENCED_CODE

    class TutsPlusRenderer(HtmlRenderer):
        def block_code(self, text, lang):
            lang = lang or 'text'
            return '\n[%s]%s[/%s]\n' % (lang, text, lang)

        def image(self, link, title, alt_text):
            return "<!-- start img --><div class='tutorial_image'><img src='%s' alt='%s' title='%s' border='0'></div><!-- end img -->" % (link, alt_text, title)

        def header(self, text, level):
            level = 2 if level == 1 else level
            elem = '\n'
            elem = '%s<hr>\n' % elem if level == 2 else elem
            elem = '%s<h%s>%s</h%s>' % (elem, level, text, level)
            return elem

    class TutsplusmarkdownCommand(sublime_plugin.TextCommand):
        def run(self, edit):
            window = sublime.active_window()
            new_file = window.new_file()
            content = self.view.substr(sublime.Region(0, self.view.size()))
            html = self.convert(content)
            new_file.insert(edit, 0, html)

        def escape_underscore(self, matchobj):
            if matchobj.group(0)[:2] != '__':
                replaced = re.sub('_', '\_', matchobj.group(0))
                return replaced
            return matchobj.group(0)

        def newline(self, matchobj):
            return re.sub(r'^(.+)$', '\1 ', matchobj.group(0))

        def convert(self, contents):
            markdown = Markdown(TutsPlusRenderer(), EXT_FENCED_CODE)

            contents = re.sub(r'(\w+_\w+_\w[\w_]*)', self.escape_underscore, contents)
            contents = re.sub(re.compile(r'(\A|^$\n)(^\w[^\n]*\n)(^\w[^\n]*$)+', re.MULTILINE), self.newline, contents)

            converted = markdown.render(contents)

            converted = re.sub(r'(<p>)?<!-- start img -->', '', converted)
            converted = re.sub(r'<!-- end img -->(</p>)?', '', converted)

            return converted
except ImportError:
    pass
