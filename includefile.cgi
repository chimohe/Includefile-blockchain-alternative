use strict;
use warnings;
use Crypt::Digest::SHA256 qw(sha256_hex);
use Crypt::RSA;
use Crypt::RSA::Key;
use File::Spec;

sub includefile {
    my ($fname, @data_array) = @_;

    # Generate a private key for signing
    my $private_key = Crypt::RSA::Key::Private->generate(Size => 2048);
    my $public_key  = $private_key->public_key();

    my $target_zeros = 4;  # Dynamic difficulty adjustment could be implemented here
    my $nonce        = 0;
    
    # Prepare the file path securely
    my $file_path = File::Spec->catfile('path_to_directory', $fname);

    # Open the file for appending
    if (!open(INCLUDE, '>>', $file_path)) {
        die "Failed to open file $file_path: $!";
    }

    foreach my $item (@data_array) {
        my $signature = $private_key->sign_string($item, 'SHA-256');

        # PoW: Find the correct nonce value
        my $data_with_nonce = "$item:$signature:$nonce";
        my $hash;
        do {
            $nonce++;
            $data_with_nonce = "$item:$signature:$nonce";
            $hash = sha256_hex($data_with_nonce);
        } while (substr($hash, 0, $target_zeros) ne "0" x $target_zeros);

        print INCLUDE "$data_with_nonce\n";
    }

    close(INCLUDE) or die "Failed to close file $file_path: $!";

    return 1;  # Indicate success
}

# Example usage with multiple arrays
my @arrays_to_append = (
    ["Block 1 data", "Block 2 data", "Block 3 data"],
    ["Block A data", "Block B data", "Block C data"],
    ["Block X data", "Block Y data", "Block Z data"]
);

for my $i (0 .. $#arrays_to_append) {
    my $filename = "blockchain$i.txt";  # Replace with desired filenames
    eval {
        includefile($filename, @{$arrays_to_append[$i]});
        print "Data successfully added to $filename.\n";
    } or do {
        my $error = $@;
        print "Error adding data to $filename: $error\n";
    };
}
