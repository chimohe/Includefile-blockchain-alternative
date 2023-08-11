use strict;
use warnings;
use Crypt::Digest::SHA256 qw(sha256_hex);
use Crypt::RSA;
use Crypt::RSA::Key;

sub includefile {
    my ($fname, @data_array) = @_;

    # Remove potentially harmful characters from the file name
    $fname =~ s/([\&;\`'\|\"*\?\~\^\(\)\[\]\{\}\$\n\r])//g;

    # Open the file for appending
    if (!open(INCLUDE, '>>', $fname)) {
        return '[an error occurred while processing this directive]';
    }

    # Generate a private key for signing
    my $private_key = Crypt::RSA::Key::Private->generate(Size => 1024);
    my $public_key  = $private_key->public_key();

    # Append the @_array data, signatures, and proof-of-work to the file
    my $target_zeros = 4;    # The required number of leading zeros in the hash
    my $nonce        = 0;
    foreach my $item (@data_array) {
        my $signature = $private_key->sign_string($item, 'SHA-256');

        # PoW: Find the correct nonce value
        my $data
