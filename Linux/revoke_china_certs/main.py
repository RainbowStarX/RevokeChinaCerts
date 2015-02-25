#!/usr/local/env python
import ssl
import M2Crypto
import hashlib
import json
import base64
import sys, os
import glob
from subprocess import Popen
from subprocess import PIPE

DEFAULT_CERT_PATH = '/usr/share/ca-certificates/'
DEFAULT_CERT_CONF = '/etc/ca-certificates.conf'
#DEFAULT_HASH_FILE = '/run/shm/revoke_china_certs.conf'
DEFAULT_HASH_FILE = '/etc/revoke_china_certs.conf'


__all__ = ['main']

def _normalize_hash(hash_val):
    return hash_val.replace('_', '').replace(':', '').upper()

def usage():
    print ""
    print "%s" % sys.argv[0]
    print ""
    print "-------------------------------------"
    print "Generate new ca-certificates.conf that revokes certs in %s according to %s." % (DEFAULT_CERT_CONF, DEFAULT_HASH_FILE)
    print "\t%s revoke" % sys.argv[0]
    print "Generate new ca-certificates.conf that revokes certs in [cert_conf] according to [revoke_list]."
    print "\t%s revoke [cert_conf] [revoke_list]"  % sys.argv[0]
    print "Generate new ca-certificates.conf that revokes certs in configurations from STDIN according to [revoke_list]."
    print "\t%s revoke - [revoke_list]" % sys.argv[0]
    print "\teg: cat /etc/ca-certificates.conf | %s revoke - [revoke_list]" % sys.argv[0]
    print "Generate revocation list"
    print "\t%s generate [certs to revoke]" % sys.argv[0]
    print "\teg: %s generate ../../Windows/Certs/Online/*" % sys.argv[0]
    print ""

def _hash_dict(files):
    result = []
    for f in files:
        try:
            m = M2Crypto.X509.load_cert(os.path.realpath(f))
            result.append(m.get_fingerprint())
        except:
            pass
    return result

def _parent_folder(path):
    return os.path.abspath(os.path.join(path, os.pardir))

def _load_dict(path):
    try:
        f = open(path, 'r')
        cont = [s.strip() for s in f.readlines()]
        f.close()
        return cont
    except:
        return []

def generate_revoke_hash():
    #print sys.argv
    assert sys.argv[1] == 'generate'
    files = sys.argv[2:]
    for s in _hash_dict(files):
        print s

def _revoke(config, dct):
    if config == '-':
        fl = sys.stdin
    else:
        fl = open(config, 'r')
    certs = fl.readlines()
    new_conf = []
    for f in certs:
        f = f.strip()
        if not len(f[0]) or f[0] in ('!', '#'):
            new_conf.append(f)
            continue
        path = os.path.realpath(os.path.join(DEFAULT_CERT_PATH, f))
        try:
            m = M2Crypto.X509.load_cert(path)
            fingerprint = m.get_fingerprint()
            if fingerprint in dct:
                new_conf.append('!' + f)
            else:
                new_conf.append(f)
        except:
            sys.stderr.write("# Warning: Failure occured processing " + path + "\n")
            new_conf.append(f)
            raise
    print '\n'.join(new_conf)

def revoke_by_hash():
    assert sys.argv[1] == 'revoke'
    cert_conf = sys.argv[2] if len(sys.argv)>=3 else DEFAULT_CERT_CONF
    blacklist_conf = sys.argv[3] if len(sys.argv)>=4 else DEFAULT_HASH_FILE
    dct = _load_dict(blacklist_conf)
    _revoke(cert_conf, dct)

def main():
    if len(sys.argv)<2:
        usage()
    elif sys.argv[1] == 'generate':
        generate_revoke_hash()
    elif sys.argv[1] == 'revoke':
        revoke_by_hash()
    else:
        usage()

if __name__ == "__main__":
    main()
