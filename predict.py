import sys
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from google.api_core.client_options import ClientOptions
from google.cloud import automl_v1
from google.cloud.automl_v1.proto import service_pb2


class LabelWindow(Gtk.Window):

 def __init__(self):
        Gtk.Window.__init__(self, title="Youcode Intelligence Solutions")
        vbox_first = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        vbox_first.set_homogeneous(False)
        vbox_last = Gtk.Box(spacing=10)
        vbox_last.set_homogeneous(False)
        hbox_top = Gtk.Box(spacing=10)
        hbox_top.set_homogeneous(False)
        hbox_top.pack_start(vbox_first, False, True, 10)
        hbox_top.pack_start(vbox_last, False, True, 10)
        self.entry = Gtk.Entry()
        self.entry.set_text("Enter the GCS location where the files are placed")
        vbox_first.pack_start(self.entry, False, True, 0)
        button = Gtk.Button.new_with_label("Start")
        button.connect("clicked", self.run)
        vbox_first.pack_start(button, False, True, 10)
        self.label1 = Gtk.Label("Output will be displayed here")
        vbox_last.pack_start(self.label1, False, True, 20)
        self.add(hbox_top)

 def inline_text_payload(self,file_path):
  with open(self.file_path, 'rb') as ff:
    content = ff.read()
  return {'text_snippet': {'content': content, 'mime_type': 'text/plain'} }

 def pdf_payload(self,file_path):
  return {'document': {'input_config': {'gcs_source': {'input_uris': [file_path] } } } }

 def get_prediction(self):
  options = ClientOptions(api_endpoint='automl.googleapis.com')
  prediction_client = automl_v1.PredictionServiceClient(client_options=options)

 #  payload = inline_text_payload(file_path)
  # Uncomment the following line (and comment the above line) if want to predict on PDFs.
  self.payload = self.pdf_payload(self.file_path)

  self.params = {}
  request = prediction_client.predict(self.model_name, self.payload, self.params)
  return request  # waits until request is returned

 def run(self,button):
  self.file_path = self.entry.get_text()
  ENTITY = ''
  OUT = ''
  self.model_name = sys.argv[1]
  response = self.get_prediction()
  for annotation_payload in response.payload:
      if(ENTITY == format(annotation_payload.display_name)):
           OUT = OUT + ': '
      else:
           OUT = OUT + '\n'
      text_segment = annotation_payload.text_extraction.text_segment
      OUT = OUT + str(format(text_segment.content))
      ENTITY = format(annotation_payload.display_name)
  self.label1.set_text(OUT) 
window = LabelWindow()        
window.connect("destroy", Gtk.main_quit)
window.show_all()
Gtk.main()
