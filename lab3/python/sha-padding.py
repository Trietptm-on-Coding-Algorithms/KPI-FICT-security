from shaext import *

key = "m7k3y"
keylen = len(key)
auth = shaauth(key)

# sign the msg
orig_msg = "Guys who understand that using Hash function as Mac is one very bad practice: Thai Duong; Juliano Rizzo; Flickr (the hard way);"
orig_sig = auth.sign(orig_msg)

# test the length extension attack
add_msg = "Yehor Borkov"
ext = shaext(orig_msg, keylen, orig_sig)
ext.add(add_msg)
(new_msg, new_sig) = ext.final()

print "orig msg: " + repr(orig_msg)
print "orig sig: " + orig_sig
print "new msg: " + repr(new_msg)
print "new sig: " + new_sig
print "Is verified: %s" % auth.verify(new_msg, new_sig)
