 #### Load pretrained model
 
 One can load our pretrained weight as a reference, just use the following code snippet
 
 ```python
# visit the link and click the mouse by oneself will work, too
!wget -q https://www.dropbox.com/s/xji5ztmtwbac296/9826model-20220910T034210Z-001.zip

# for windows user, you might have to manually unzip the file
!unzip 9826model-20220910T034210Z-001.zip

import tensorflow as tf
model = tf.keras.models.load_model("9826model")
model.evaluate(x_test,y_test)
 ```
  
