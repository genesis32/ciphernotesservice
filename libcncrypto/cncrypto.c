#include <stdio.h>
#include <assert.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#include <openssl/pem.h>
#include <openssl/aes.h>

#define AES_KEYSIZE_BYTES 256

void generate_aeskey(unsigned char *outkey, int len) {
    RAND_load_file("/dev/urandom", 128);
    int enoughData = RAND_status();
    assert(enoughData == 1);

    RAND_bytes(outkey, len);
}

void rsa_encrypt(const char *pemkey, const unsigned char *plaintext, unsigned char *ciphertext, int *ciphertext_len) {
    BIO *mem = BIO_new_mem_buf((void *)pemkey, strlen(pemkey));
    
    RSA *rkey = NULL;
    PEM_read_bio_RSA_PUBKEY(mem, &rkey, NULL, NULL);
    
    BIO_free(mem);

   // *ciphertext = (unsigned char *)malloc(RSA_size(rkey));
   
    int ptlen = (int)strlen((const char *)plaintext);
    *ciphertext_len = RSA_public_encrypt(ptlen, plaintext, ciphertext, rkey, RSA_PKCS1_PADDING);
}

void aes_decrypt(const char *aeskey, unsigned char *ciphertext, int ciphertext_len, unsigned char *plaintext, int *plaintext_len) {
    
    unsigned char salt[] = { 0, 1, 2, 3, 0, 1, 2, 3};
    
    EVP_CIPHER_CTX ectx;
    int i, nrounds = 5;
    unsigned char key[32], iv[32];
    
    i = EVP_BytesToKey(EVP_aes_256_cbc(), EVP_sha1(), salt, (unsigned char *)aeskey, AES_KEYSIZE_BYTES, nrounds, key, iv);
    assert(i == 32);
    
    EVP_CIPHER_CTX_init(&ectx);
    EVP_DecryptInit_ex(&ectx, EVP_aes_256_cbc(), NULL, key, iv);
    
    int len = ciphertext_len; 
    int plen = 0;
    int flen = 0;
    
    EVP_DecryptInit_ex(&ectx, NULL, NULL, NULL, NULL);
    EVP_DecryptUpdate(&ectx, plaintext, &plen, ciphertext, len);
    EVP_DecryptFinal_ex(&ectx, plaintext+plen, &flen);
    
    *plaintext_len = plen + flen;

    EVP_CIPHER_CTX_cleanup(&ectx);
}      

void aes_encrypt(const char *aeskey, const unsigned char *plaintext, unsigned char *ciphertext, int *ciphertext_len) {
    unsigned char salt[] = { 0, 1, 2, 3, 0, 1, 2, 3};
    
    EVP_CIPHER_CTX ectx;
    int i, nrounds = 5;
    unsigned char key[32], iv[32];
    
    i = EVP_BytesToKey(EVP_aes_256_cbc(), EVP_sha1(), salt, (unsigned char *)aeskey, AES_KEYSIZE_BYTES, nrounds, key, iv);
    assert(i == 32);
    
    EVP_CIPHER_CTX_init(&ectx);
    EVP_EncryptInit_ex(&ectx, EVP_aes_256_cbc(), NULL, key, iv);
    
    int plaintext_len = (int)strlen((const char *)plaintext);
    size_t olen = plaintext_len + 1;
    
    int clen = olen + AES_BLOCK_SIZE;
    int flen = 0;

    EVP_EncryptInit_ex(&ectx, NULL, NULL, NULL, NULL);
    EVP_EncryptUpdate(&ectx, ciphertext, &clen, plaintext, olen);
    EVP_EncryptFinal(&ectx, ciphertext + clen, &flen);

    *ciphertext_len = clen + flen;
            
    EVP_CIPHER_CTX_cleanup(&ectx);
}
/*
int main(int argc, char *argv[]) {
    const char *passwd = "test";
    const char *input  = "abcdef";

    int cipherlen;
    unsigned char cipheroutput[256] = { 0 };
    aes_encrypt(passwd, (unsigned char *)input, cipheroutput, &cipherlen);

    int plainlen;
    unsigned char plainoutput[256] = { 0 }; 
    aes_decrypt(passwd, cipheroutput, cipherlen, plainoutput, &plainlen);
    printf("%s\n", plainoutput);

    free(cipheroutput);
    free(plainoutput);

    return 0;
}
*/ 
