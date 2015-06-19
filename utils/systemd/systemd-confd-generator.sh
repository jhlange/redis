#!/bin/sh

# More details about systemd generator:
# http://www.freedesktop.org/wiki/Software/systemd/Generators/
printUsage() {
  echo "Usage: $0 <conf.d_directory> <instance_template_file> [wants_directory]" 1>&2
  echo "" 1>&2
  echo "e.x. $0 /etc/myservice/conf.d  /usr/lib/systemd/system/myservice-config@.service  /usr/lib/systemd/system/myservice.service.wants" 1>&2
}

conf_d_dir="$1"
src_template="$2"
dest_wants="$3"

is_test_mode=0
if [  "$dest_wants" = "" ]; then
    dest_wants="/tmp/usr/lib/systemd/system/myservice.service.wants"
    echo "TESTING MODE: managing symlinks in $dest_wants"
fi

if ! [ -d "$conf_d_dir" ]; then
    echo "$conf_d_dir does not exist" 2>&1
    printUsage
    exit 1
fi
if ! [ -f "$src_template" ]; then
    echo "$src_template does not exist" 2>&1
    printUsage
    exit 1
fi

###################################################################
###################################################################
# In the 99% case we dont have to re-link. lets waste some cpu to make sure that we actually have to
# a write before we do.

if ! [ -d "$dest_wants" ]; then
    mkdir -p "$dest_wants"
fi

if ! [ -d "$dest_wants" ]; then
  echo "Failed to make $dest_wants directory" 1>&2
  printUsage
  exit 1
fi

src_template_file_name="${src_template##*/}" # e.g.  redis-server-inst@.service or possibly .targeti
src_template_suffix="${src_template_file_name##*@}" # = .service
src_template_base_name="${src_template_file_name%@*}" # = redis-server-inst
if [ "${src_template_base_name}@${src_template_suffix}" != "${src_template_file_name}" ] || [ "$src_template_suffix" = "" ] || [ "$src_template_base_name" = "" ]; then
    echo "Missing @ in template service name" 1>&2
    printUsage
    exit 1
fi

# Step 1, remove all of the extras
for each_want in $dest_wants/*${src_template_suffix}; do
    if [ -L "$each_want" ] ; then
        each_file_name="${each_want##*/}"
        each_file_name_no_extension="${each_file_name%$src_template_suffix}"
        if [ "$each_file_name_no_extension" != "" ] && [ "${each_file_name:0:1}" != "." ] && ! [ -e "${conf_d_dir}/${each_file_name_no_extension}.conf" ]; then
            echo unlink "$each_want"
        fi
    fi
done

# Step 2, add all the missing
for each_new in $conf_d_dir/*.conf; do
    each_file_name="${each_new##*/}"
    each_file_name_no_extension="${each_file_name%.conf}"
    if [ "$each_file_name_no_extension" != "" ] && [ "${each_file_name:0:1}" != "." ] && ! [ -L "$dest_wants/${each_file_name_no_extension}${src_template_suffix}" ]; then
        echo ln -s "$src_template" "${dest_wants}/${src_template_base_name}@${each_file_name_no_extension}${src_template_suffix}"
    fi
done
