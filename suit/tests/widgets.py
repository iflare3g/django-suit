from django import VERSION
from django.test import TestCase
from suit.widgets import LinkedSelect, HTML5Input, EnclosedInput, \
    NumberInput, SuitDateWidget, SuitTimeWidget, SuitSplitDateTimeWidget, \
    AutosizedTextarea
from django.utils.translation import gettext_lazy as _

from django.templatetags.static import static

DJANGO_VERSION = VERSION[:2]


class WidgetsTestCase(TestCase):
    def test_NumberInput(self):
        inp = NumberInput()
        self.assertEqual('number', inp.input_type)

    def test_HTML5Input(self):
        input_type = 'calendar'
        inp = HTML5Input(input_type=input_type)
        self.assertEqual(input_type, inp.input_type)

    def test_LinkedSelect(self):
        ls = LinkedSelect()
        self.assertTrue('linked-select' in ls.attrs['class'])

    def test_LinkedSelect_with_existing_attr(self):
        ls = LinkedSelect(attrs={'class': 'custom-class', 'custom': 123})
        self.assertEqual('linked-select custom-class', ls.attrs['class'])
        self.assertEqual(ls.attrs['custom'], 123)

    def render_enclosed_widget(self, enclosed_widget):
        return enclosed_widget.render('enc', 123)

    def get_enclosed_widget_html(self, values):
        return '<div class="input-prepend input-append">%s<input name="enc" ' \
               'type="text" value="123" />%s</div>' % values

    def test_EnclosedInput_as_text(self):
        inp = EnclosedInput(prepend='p', append='a')
        output = self.render_enclosed_widget(inp)
        result = ('<span class="add-on">p</span>',
                  '<span class="add-on">a</span>')
        self.assertHTMLEqual(output, self.get_enclosed_widget_html(result))

    def test_EnclosedInput_as_icon(self):
        inp = EnclosedInput(prepend='icon-fire', append='icon-leaf')
        output = self.render_enclosed_widget(inp)
        result = ('<span class="add-on"><i class="icon-fire"></i></span>',
                  '<span class="add-on"><i class="icon-leaf"></i></span>')
        self.assertHTMLEqual(output, self.get_enclosed_widget_html(result))

    def test_EnclosedInput_as_html(self):
        inp = EnclosedInput(prepend='<em>p</em>', append='<em>a</em>')
        output = self.render_enclosed_widget(inp)
        result = ('<em>p</em>', '<em>a</em>')
        self.assertHTMLEqual(output, self.get_enclosed_widget_html(result))

    def test_SuitDateWidget(self):
        sdw = SuitDateWidget()
        self.assertTrue('vDateField' in sdw.attrs['class'])

    def test_SuitDateWidget_with_existing_class_attr(self):
        sdw = SuitDateWidget(attrs={'class': 'custom-class'})
        self.assertTrue('vDateField ' in sdw.attrs['class'])
        self.assertTrue(' custom-class' in sdw.attrs['class'])
        self.assertEqual(_('Date:')[:-1], sdw.attrs['placeholder'])

    def test_SuitDateWidget_with_existing_placeholder_attr(self):
        sdw = SuitDateWidget(attrs={'class': 'custom-cls', 'placeholder': 'p'})
        self.assertTrue('vDateField ' in sdw.attrs['class'])
        self.assertTrue(' custom-cls' in sdw.attrs['class'])
        self.assertEqual('p', sdw.attrs['placeholder'])

    def test_SuitDateWidget_output(self):
        sdw = SuitDateWidget(attrs={'placeholder': 'Date'})
        output = sdw.render('sdw', '')
        self.assertIn('input-append suit-date', output)
        self.assertIn('vDateField', output)
        self.assertIn('input-small', output)
        self.assertIn('placeholder="Date"', output)
        self.assertIn('name="sdw"', output)
        self.assertIn('add-on', output)
        self.assertIn('icon-calendar', output)

    def test_SuitTimeWidget(self):
        sdw = SuitTimeWidget()
        self.assertTrue('vTimeField' in sdw.attrs['class'])

    def test_SuitTimeWidget_with_existing_class_attr(self):
        sdw = SuitTimeWidget(attrs={'class': 'custom-class'})
        self.assertTrue('vTimeField ' in sdw.attrs['class'])
        self.assertTrue(' custom-class' in sdw.attrs['class'])
        self.assertEqual(_('Time:')[:-1], sdw.attrs['placeholder'])

    def test_SuitTimeWidget_with_existing_placeholder_attr(self):
        sdw = SuitTimeWidget(attrs={'class': 'custom-cls', 'placeholder': 'p'})
        self.assertTrue('vTimeField ' in sdw.attrs['class'])
        self.assertTrue(' custom-cls' in sdw.attrs['class'])
        self.assertEqual('p', sdw.attrs['placeholder'])

    def test_SuitTimeWidget_output(self):
        sdw = SuitTimeWidget(attrs={'placeholder': 'Time'})
        output = sdw.render('sdw', '')
        self.assertIn('input-append suit-date suit-time', output)
        self.assertIn('vTimeField', output)
        self.assertIn('input-small', output)
        self.assertIn('placeholder="Time"', output)
        self.assertIn('name="sdw"', output)
        self.assertIn('add-on', output)
        self.assertIn('icon-time', output)

    def test_SuitSplitDateTimeWidget(self):
        ssdtw = SuitSplitDateTimeWidget()
        output = ssdtw.render('sdw', '')
        self.assertIn('datetime', output)
        self.assertIn('vDateField', output)
        self.assertIn('vTimeField', output)
        self.assertIn('name="sdw_0"', output)
        self.assertIn('name="sdw_1"', output)
        self.assertIn('placeholder="Date"', output)
        self.assertIn('placeholder="Time"', output)

    def test_AutosizedTextarea(self):
        txt = AutosizedTextarea()
        self.assertTrue('autosize' in txt.attrs['class'])
        self.assertEqual(2, txt.attrs['rows'])

    def test_AutosizedTextarea_with_existing_attrs(self):
        txt = AutosizedTextarea(attrs={'class': 'custom-class', 'rows': 3})
        self.assertTrue('autosize ' in txt.attrs['class'])
        self.assertTrue(' custom-class' in txt.attrs['class'])
        self.assertEqual(txt.attrs['rows'], 3)

    def test_AutosizedTextarea_output(self):
        txt = AutosizedTextarea()
        output = txt.render('txt', '')
        self.assertIn('autosize', output)
        self.assertIn('name="txt"', output)
        self.assertIn('rows="2"', output)
        self.assertIn("Suit.$('#id_txt').autosize();", output)

    def test_AutosizedTextarea_media(self):
        txt = AutosizedTextarea()
        js_url = static('suit/js/jquery.autosize-min.js')
        media_str = str(txt.media)
        self.assertIn(js_url, media_str)
        self.assertIn('<script', media_str)
