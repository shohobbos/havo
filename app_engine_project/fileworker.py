#Bu biblioteka google apps engine'dagi
#UzStudio proektlari uchun ishlab chiqarilgan.
#Bu bibliotekani faqat moddiy foyda 
#keltirmaydigan proektlarda ishlatish mumkin!


import logging
import os
import cloudstorage as gcs
import webapp2

from google.appengine.api import app_identity


my_default_retry_params = gcs.RetryParams(initial_delay=0.2,
                                          max_delay=5.0,
                                          backoff_factor=2,
                                          max_retry_period=15)
gcs.set_default_retry_params(my_default_retry_params)
#[END retries]

class open:
    def __init__(self, way, mode):
        bucket_name = os.environ.get('BUCKET_NAME',
                                 app_identity.get_default_gcs_bucket_name())
        bucket = '/' + bucket_name
        self.way = bucket + "/" + way.replace("./","",1)
        self.mode = mode
    def write(self, data):
      if self.mode == 'a':
        try:
          file=gcs.open(self.way)
          dataOld=file.read()
          file.close()
        except:
          dataOld = ''
        write_retry_params = gcs.RetryParams(backoff_factor=1.1)
        file=gcs.open(self.way, 'w', content_type='text/plain', retry_params=write_retry_params)
        file.write(dataOld + data.encode('utf-8'))
        file.close()
        return("ok")
      else:
        write_retry_params = gcs.RetryParams(backoff_factor=1.1)
        file=gcs.open(self.way, self.mode, content_type='text/plain', retry_params=write_retry_params)
        file.write(data.encode('utf-8'))
        file.close()
        return("ok")
    def read(self, A=None):
        try:
            A = int(A)
            file=gcs.open(self.way)
            data=file.read()
            file.close()
            data = data[:A]
            return(data)
        except:
            file=gcs.open(self.way)
            data=file.read()
            file.close()
            return(data)
    
    
