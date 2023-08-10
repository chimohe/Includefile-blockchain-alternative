use strict;
use warnings;
use Crypt::OpenSSL::RSA;
use Crypt::PRNG qw(random_bytes);
use Digest::SHA qw(sha256_hex);
use Crypt::SaltedHash;

# Constants
my $KEY_SIZE = 4096;            # Increased key size for stronger security
my $TARGET_ZEROS = 6;           # Increased proof-of-work difficulty

sub includefile {
    my ($fname, @array) = @_;

    die "Invalid filename: $fname" unless $fname =~ /^[A-Za-z0-9_\-\.]+$/;

    my $rsa = Crypt::OpenSSL::RSA->generate_key($KEY_SIZE);
    my $private_key = $rsa->get_private_key_string();
    my $public_key = $rsa->get_public_key_string();

    my $nonce = generate_nonce();

    open my $fh, '>>', $fname or die "Cannot open $fname: $!";

    foreach my $item (@array) {
        validate_data($item);

        my $signature = $rsa->sign($item, 'SHA-256');

        my $data_with_nonce = "$item:$signature:$nonce";
        my $hash = sha256_hex($data_with_nonce);

        while (substr($hash, 0, $TARGET_ZEROS) ne "0" x $TARGET_ZEROS) {
            $nonce = generate_nonce();
            $data_with_nonce = "$item:$signature:$nonce";
            $hash = sha256_hex($data_with_nonce);
        }

        print $fh "$data_with_nonce\n";
    }

    close($fh);

    return 1;
}

sub validate_data {
    my ($data) = @_;
    die "Invalid data" unless defined $data && length($data) > 0;
}

sub generate_nonce {
    return unpack("L", random_bytes(4));  # Using Crypt::PRNG for better security
}

sub generate_salted_hash {
    my ($data) = @_;
    my $csh = Crypt::SaltedHash->new(algorithm => 'SHA-512');
    $csh->add($data);
    return $csh->generate;
}

my $filename = "blockchain.txt";
my @data_to_append = ("Block 1 data", "Block 2 data", "Block 3 data");

my $result = includefile($filename, @data_to_append);
if ($result) {
    print "Data successfully added to the blockchain file.\n";
} else {
    print "Error adding data to the blockchain file.\n";
}
