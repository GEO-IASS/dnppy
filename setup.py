import os
import shutil
import sys
import time

import dnppy_install


"""
 This is a barebones install script to install the dnppy module
 
 It simply checks the version numbers indicated in __init__.py and
 copies the dnppy_install folder contents into a new folder named
 dnppy in the site-packages folder in the currently running python library.

 It duplicates this action for a version specific named folder so users can
 switch back and forth between old and new versions by explicitly importing,
 for example:

   from dnppy0.0.2     import core as old_core
   from dnppy1.15.1    import core as new_core

 If you have knowledge of distutils and wish to make this installation more
 professional and cleaner, feel free to do so!
"""

# determine if the version being installed is newer than the current version
def upgrading(now_ver, up_ver):
    now = now_ver.split('.')
    up  = up_ver.split('.')
    length = min([len(now),len(up)])
    for i in range(length):
        now[i] = now[i].ljust(5,'0')
        up[i]  = up[i].ljust(5,'0')
    if int(''.join(up)) >= int(''.join(now)):
        return True
    return False

print("====================================================================")
print("   Setting up dnnpy! the DEVELOP National Program python package!")
print("====================================================================\n")

up_vers = dnppy_install.__version__

library_path, _ = os.path.split(os.__file__)
source_path, _  = os.path.split(dnppy_install.__file__)
dest_path       = os.path.join(library_path, 'site-packages','dnppy')
dest_path2      = dest_path + up_vers

if os.path.isdir(dest_path):
    
    try:
        import dnppy
    
        now_vers = dnppy.__version__

        if upgrading(now_vers , up_vers):
            print("Updating from dnppy version [{0}] to version [{1}]...".format(now_vers, up_vers))
            
            time.sleep(0)   # people seem to think an error has occured when it installs too quickly.
                            # this gives people time to actually read the screen.
            
            shutil.rmtree(dest_path)
            shutil.copytree(source_path, dest_path)

            if os.path.isdir(dest_path2):
                shutil.rmtree(dest_path2)
            shutil.copytree(source_path, dest_path2)

        else:
            print("you are trying to replace your dnppy with an older version!")
            print("Are you sure you wish to downgrade")
            downgrade = raw_input("from version [{0}] to [{1}]? (y/n): ".format(now_vers, up_vers))
            if downgrade == 'y' or downgrade == 'Y':
                shutil.rmtree(dest_path)
                shutil.copytree(source_path, dest_path)
                shutil.rmtree(dest_path2)
                shutil.copytree(source_path, dest_path2)
            else:
                print("Setup aborted!")
                
    except ImportError:
        shutil.rmtree(dest_path)
        shutil.rmtree(dest_path2)
        print("installing dnppy version [{0}]".format(up_vers))
        shutil.copytree(source_path, dest_path)
        shutil.copytree(source_path, dest_path2)
else:
    print("installing dnppy version [{0}]".format(up_vers))
    shutil.copytree(source_path, dest_path)
    shutil.copytree(source_path, dest_path2)
    

print('\nSource path       : ' + source_path)
print('Destination path 1: ' + dest_path)
print('Destination path 2: ' + dest_path2)

print "\nSetup finished!"
print("Window will close in 10 seconds")
time.sleep(10)
sys.exit()

