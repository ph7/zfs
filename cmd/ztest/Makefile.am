include $(top_srcdir)/config/Rules.am

AUTOMAKE_OPTIONS = subdir-objects

AM_CFLAGS += $(DEBUG_STACKFLAGS) $(FRAME_LARGER_THAN)

DEFAULT_INCLUDES += \
	-I$(top_srcdir)/include \
	-I$(top_srcdir)/lib/libspl/include

sbin_PROGRAMS = ztest ztest_static

ztest_SOURCES = \
	ztest.c

ztest_LDADD = \
	$(top_builddir)/lib/libnvpair/libnvpair.la \
	$(top_builddir)/lib/libuutil/libuutil.la \
	$(top_builddir)/lib/libzpool/libzpool.la \
	$(top_builddir)/lib/libzfs/libzfs.la

ztest_LDFLAGS = -pthread -lm $(ZLIB) -ldl $(LIBUUID) $(LIBBLKID)


ztest_static_SOURCES = \
	$(top_srcdir)/cmd/ztest/ztest.c

ztest_static_LDADD = \
	$(top_builddir)/lib/libnvpair/libnvpair.la \
	$(top_builddir)/lib/libuutil/libuutil.la \
	$(top_builddir)/lib/libzpool/libzpool.la \
	$(top_builddir)/lib/libzfs/libzfs.la

ztest_static_LDFLAGS = -static -pthread -lm $(ZLIB) -ldl $(LIBUUID) $(LIBBLKID)
