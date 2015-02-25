Revoke-China-Certs for Ubuntu
=========================================

## Intro

This tool disables certain CA certificates on Ubuntu.

It's tested on Ubuntu 12.04+ (should also work with Debian/LinuxMint).

## Proceed with predefined blacklist

        git clone [GIT_REPO]
        cd RevokeChinaCerts/Linux/
        sudo pip install .
        # Make a backup
        cp /etc/ca-certificates.conf /etc/ca-certificates.conf.bak
        # Reconfigure the CA list. [Type] can be ALL, BASE, EXTENDED
        cat /etc/ca-certificates.conf | revoke-china-certs revoke - ./revoke-china-certs.[TYPE].conf | \
                tee /tmp/ca-certificates.conf
        # Replace CA list
        sudo mv /tmp/ca-certificates.conf /etc/ca-certificates.conf

However, any future updates from package `ca-certificates` may override this.
To mitigate the problem, use `cron` to run the fix routinely.

        # Choose the type you want
        sudo cp ./revoke-china-certs.[TYPE].conf /etc/revoke-china-certs.conf

Then use cron to run the following command routinely (as root):

        # Run every 6 hours as root.
        * */6    *    *    *		root	(revoke-china-certs revoke >/tmp/ca-certificates.conf; cp /tmp/ca-certificates.conf /etc/ca-certificates.conf)

You can also add
`(revoke-china-certs revoke >/tmp/ca-certificates.conf; cp /tmp/ca-certificates.conf /etc/ca-certificates.conf)`
 to `.bashrc` or whatever script that is routinely invoked.

## Generate custom blacklist

To generate a custom blacklist, use `pip` to install the package as described above. Then:

        revoke-china-certs generate [certificates to revoke]

For example:

        revoke-china-certs generate ~/RevokeChinaCerts/Windows/Online/* | tee /tmp/revoke.txt

Then, the file `/tmp/revoke.txt` is in the same format as `revoke-china-certs.ALL.conf` and
can be used the same way.

## Validation tool

Run `./validator.sh` to test. On a machine with `EXTENDED` certs revoked, you should see:

        ---------------------
        Beginning tests.
        There are 3 tests (BASE/EXTENDED/ALL), each of which would print a  'Passed test' if passes
        ---------------------
        Passed test sites for BASE incremental-set
        Passed test sites for EXTENDED incremental-set
        Failed test sites for ALL incremental-set
        ---------------------
        All tests executed.


## Notes

As mentioned above, updates from the package `ca-certificates` may very well
install a new certificates from, say, WoSign, but *RevokeChinaCerts* is not
able to prevent that *ahead of time*.


