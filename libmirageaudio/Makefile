
LIBS := gstreamer-1.0 glib-2.0 fftw3 fftw3f samplerate
CFLAGS += $(shell pkg-config --cflags ${LIBS})
LDFLAGS += $(shell pkg-config --libs ${LIBS})

#-I /usr/include/glib-2.0/ -I /usr/lib64/glib-2.0/include/ -lgstreamer-1.0 -I /usr/include/gstreamer-1.0/ 

libmirageaudio.so: gst-mirageaudio.c gst-mirageaudio.h
	gcc ${CFLAGS} ${LDFLAGS} -shared -fPIC $< -o $@

mirageaudiotest.exe: libmirageaudio.so mirageaudiotest.c
	gcc ${CFLAGS} ${LDFLAGS} $^ -o $@
