# Power on Bluetooth using bluetoothctl
bluetoothctl << EOF
power on
quit
EOF

# Or manually:
echo "power on" | bluetoothctl


# Copy Python D-Bus modules
scp -r output/target/usr/lib/python3.11/site-packages/dbus* user@nuc980:/usr/lib/python3.11/site-packages/
scp -r output/target/usr/lib/python3.11/site-packages/gi* user@nuc980:/usr/lib/python3.11/site-packages/
scp -r output/target/usr/lib/python3.11/site-packages/_dbus* user@nuc980:/usr/lib/python3.11/site-packages/

# Copy D-Bus shared libraries
scp output/target/usr/lib/libdbus-*.so* user@nuc980:/usr/lib/
scp output/target/usr/lib/libglib-*.so* user@nuc980:/usr/lib/
scp output/target/usr/lib/libgobject-*.so* user@nuc980:/usr/lib/
scp output/target/usr/lib/libgio-*.so* user@nuc980:/usr/lib/


scp -r joseph@10.22.22.107:/home/joseph/project/nuc980/buildroot_2024/output/target/usr/lib/python3.11/site-packages/dbus* /data/usr/lib/python3.11/site-packages/
scp -r joseph@10.22.22.107:/home/joseph/project/nuc980/buildroot_2024/output/target/usr/lib/python3.11/site-packages/gi* /data/usr/lib/python3.11/site-packages/
scp -r joseph@10.22.22.107:/home/joseph/project/nuc980/buildroot_2024/output/target/usr/lib/python3.11/site-packages/_dbus* /data/usr/lib/python3.11/site-packages/


# Copy GI Python modules xxx
scp -r joseph@10.22.22.107:/home/joseph/project/nuc980/buildroot_2024/output/target/usr/lib/python3.11/site-packages/gi /data/usr/lib/python3.11/site-packages/

# Copy GI shared libraries  
scp joseph@10.22.22.107:/home/joseph/project/nuc980/buildroot_2024/output/target/usr/lib/libgirepository-*.so* /data/usr/lib/ xxx
scp joseph@10.22.22.107:/home/joseph/project/nuc980/buildroot_2024/output/target/usr/lib/libffi.so* /data/usr/lib/

# Copy GI typelib data   xxxx
scp -r joseph@10.22.22.107:/home/joseph/project/nuc980/buildroot_2024/output/target/usr/lib/girepository-1.0 /data/usr/lib/
scp -r joseph@10.22.22.107:/home/joseph/project/nuc980/buildroot_2024/output/target/usr/share/gir-1.0 /data/usr/share/

# Copy GLib libraries (required by GI)
scp joseph@10.22.22.107:/home/joseph/project/nuc980/buildroot_2024/output/target/usr/lib/libglib-2.0.so* /data/usr/lib/
scp joseph@10.22.22.107:/home/joseph/project/nuc980/buildroot_2024/output/target/usr/lib/libgobject-2.0.so* /data/usr/lib/
scp joseph@10.22.22.107:/home/joseph/project/nuc980/buildroot_2024/output/target/usr/lib/libgio-2.0.so* /data/usr/lib/



# Copy the dbus_next Python module
scp -r joseph@10.22.22.107:/home/joseph/project/nuc980/buildroot_2024/output/target/usr/lib/python3.11/site-packages/dbus_next /data/usr/lib/python3.11/site-packages/

# Also copy any dbus_next related files
scp -r joseph@10.22.22.107:/home/joseph/project/nuc980/buildroot_2024/output/target/usr/lib/python3.11/site-packages/dbus_next-* /data/usr/lib/python3.11/site-packages/

### copy gobject
 # Copy Python GI modules
scp -r joseph@10.22.22.107:/home/joseph/project/nuc980/buildroot_2024/output/target/usr/lib/python3.11/site-packages/gi /data/usr/lib/python3.11/site-packages/

scp -r joseph@10.22.22.107:/home/joseph/project/nuc980/buildroot_2024/output/target/usr/lib/python3.11/site-packages/PyGObject-* /data/usr/lib/python3.11/site-packages/

# Copy GObject shared libraries
scp joseph@10.22.22.107:/home/joseph/project/nuc980/buildroot_2024/output/target/usr/lib/libgobject-2.0.so* /data/usr/lib/
scp joseph@10.22.22.107:/home/joseph/project/nuc980/buildroot_2024/output/target/usr/lib/libglib-2.0.so* /data/usr/lib/
scp joseph@10.22.22.107:/home/joseph/project/nuc980/buildroot_2024/output/target/usr/lib/libgio-2.0.so* /data/usr/lib/
scp joseph@10.22.22.107:/home/joseph/project/nuc980/buildroot_2024/output/target/usr/lib/libgirepository-1.0.so* /data/usr/lib/
scp joseph@10.22.22.107:/home/joseph/project/nuc980/buildroot_2024/output/target/usr/lib/libffi.so* /data/usr/lib/

# Copy GI typelibs (introspection data)
scp -r joseph@10.22.22.107:/home/joseph/project/nuc980/buildroot_2024/output/target/usr/lib/girepository-1.0 /data/usr/lib/

# Copy GIR files
scp -r joseph@10.22.22.107:/home/joseph/project/nuc980/buildroot_2024/output/target/usr/share/gir-1.0 /data/usr/share/

# Copy any compiled GI extensions
scp joseph@10.22.22.107:/home/joseph/project/nuc980/buildroot_2024/output/target/usr/lib/python3.11/site-packages/gi/*.so /data/usr/lib/python3.11/site-packages/gi/