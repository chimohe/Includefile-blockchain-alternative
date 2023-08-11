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
        my $data_with_nonce = "$item:$signature:$nonce";
        my $hash            = sha256_hex($data_with_nonce);
        while (substr($hash, 0, $target_zeros) ne "0" x $target_zeros) {
            $nonce++;
            $data_with_nonce = "$item:$signature:$nonce";
            $hash            = sha256_hex($data_with_nonce);
        }

        print INCLUDE "$data_with_nonce\n";
    }

    # Close the file
    close(INCLUDE);

    return 1;    # Indicate success
}

# Example usage with multiple arrays
my @arrays_to_append = (
    ["Block 1 data", "Block 2 data", "Block 3 data"],
    ["Block A data", "Block B data", "Block C data"],
    ["Block X data", "Block Y data", "Block Z data"]
);

for my $i (0 .. $#arrays_to_append) {
    my $filename = "blockchain$i.txt"; # Replace with desired filenames
    my $result = includefile($filename, @{$arrays_to_append[$i]});
    
    if ($result) {
        print "Data successfully added to $filename.\n";
    } else {
        print "Error adding data to $filename.\n";
    }
}
