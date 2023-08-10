<?php
use Crypt_OpenSSL_RSA;
use Crypt_PRNG;
use Digest_SHA;
use Crypt_SaltedHash;

// Constants
$KEY_SIZE = 4096;
$TARGET_ZEROS = 6;

function includefile($fname, $array) {
    if (!preg_match('/^[A-Za-z0-9_\-\.]+$/', $fname)) {
        die("Invalid filename: $fname");
    }

    $rsa = new Crypt_OpenSSL_RSA();
    $rsa->generate_key($KEY_SIZE);
    $private_key = $rsa->get_private_key_string();
    $public_key = $rsa->get_public_key_string();

    $nonce = generate_nonce();

    $fh = fopen($fname, 'a') or die("Cannot open $fname");

    foreach ($array as $item) {
        validate_data($item);

        $signature = $rsa->sign($item, 'SHA-256');

        $data_with_nonce = "$item:$signature:$nonce";
        $hash = Digest_SHA::sha256_hex($data_with_nonce);

        while (substr($hash, 0, $TARGET_ZEROS) !== str_repeat('0', $TARGET_ZEROS)) {
            $nonce = generate_nonce();
            $data_with_nonce = "$item:$signature:$nonce";
            $hash = Digest_SHA::sha256_hex($data_with_nonce);
        }

        fwrite($fh, "$data_with_nonce\n");
    }

    fclose($fh);

    return true;
}

function validate_data($data) {
    if (!isset($data) || strlen($data) <= 0) {
        die("Invalid data");
    }
}

function generate_nonce() {
    return unpack("L", Crypt_PRNG::random_bytes(4));
}

function generate_salted_hash($data) {
    $csh = new Crypt_SaltedHash(array('algorithm' => 'SHA-512'));
    $csh->add($data);
    return $csh->generate();
}

$filename = "blockchain.txt";
$data_to_append = array("Block 1 data", "Block 2 data", "Block 3 data");

$result = includefile($filename, $data_to_append);
if ($result) {
    echo "Data successfully added to the blockchain file.\n";
} else {
    echo "Error adding data to the blockchain file.\n";
}
?>
