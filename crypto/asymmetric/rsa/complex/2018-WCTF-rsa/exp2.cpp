#include <algorithm>
#include <cstdint>
#include <cstdio>
#include <gmp.h>
#include <iomanip>
#include <iostream>
#include <mutex>
#include <openssl/sha.h>
#include <thread>
#include <vector>

constexpr const uint32_t nums[] = {
    // extraced from binary
    0x0E576698C, 0x0150441B5, 0x0BD08E9BD, 0x0DF15EE4D,
    0x0C8A967B1, 0x0B84BFC73, 0x02A6F1FA8, 0x018A948B4,
};

constexpr const uint32_t m = 0x3B9ACA07;
constexpr const size_t thread_num = 16;

constexpr const uint64_t N = 13677534082369767711uLL;
constexpr const uint32_t b_idx_list[2] = {683101175, 380087137};

mpz_t mod, n64, one, n, e, c;

struct __attribute__((packed)) Candidate {
  uint64_t p;
  uint32_t t;
  bool operator<(const Candidate &rhs) const { return p < rhs.p; }
};

Candidate *candidates;
uint8_t *bitvec;
constexpr const size_t bitvec_size = 1u << 29u;
std::mutex io_mtx;

void hash_thread(uint32_t lo, uint32_t hi) {
  uint32_t buf[9];
  uint8_t digest[64];
  std::copy(nums, nums + 8, buf);
  mpz_t blow;
  for (uint32_t b_idx = 0; b_idx < 2; ++b_idx) {
    buf[8] = b_idx_list[b_idx];
    SHA512((uint8_t *)buf, 36, digest);
    mpz_init(blow);
    for (int j = 0; j < 64; ++j) {
      uint32_t tmp = digest[j];
      mpz_mul_ui(blow, blow, 256);
      mpz_add_ui(blow, blow, tmp);
    }
    for (uint32_t i = lo; i < hi; ++i) {
      if ((i & 0xffffff) == 0) {
        std::lock_guard<std::mutex> l(io_mtx);
        printf("hash %x\n", i);
      }
      buf[8] = i;
      SHA512((uint8_t *)buf, 36, digest);
      mpz_t num, zero, tmp;
      mpz_init(num);
      mpz_init(zero);
      mpz_init(tmp);
      for (int j = 0; j < 64; ++j) {
        uint32_t tmp = digest[j];
        mpz_mul_ui(num, num, 256);
        mpz_add_ui(num, num, tmp);
      }
      mpz_mul_2exp(num, num, 512);
      mpz_add(num, num, blow);
      mpz_mod(tmp, n, num);
      if (mpz_cmp(tmp, zero) == 0) {
        mpz_t q, phin, d, plain;
        mpz_init(q);
        mpz_init(phin);
        mpz_init(d);
        mpz_init(plain);
        mpz_cdiv_q(q, n, num);
        gmp_printf("p = %Zd\n",num);
        gmp_printf("q = %Zd\n",q);
        mpz_sub_ui(num, num, 1);
        mpz_sub_ui(q, q, 1);
        mpz_mul(phin, q, num);
        mpz_invert(d, e, phin);
        mpz_powm(plain, c, d, n);
        gmp_printf("plain text %Zd\n",plain);
        mpz_clear(q);
        mpz_clear(phin);
        mpz_clear(d);
        mpz_clear(plain);
      }
      mpz_clear(num);
      mpz_clear(zero);
      mpz_clear(tmp);
    }
  }
  mpz_clear(blow);
}

// https://stackoverflow.com/questions/6248723/mpz-t-to-unsigned-long-long-conversion-gmp-lib
void mpz_set_ull(mpz_t n, unsigned long long ull) {
  mpz_set_ui(n, (unsigned int)(ull >> 32)); /* n = (unsigned int)(ull >> 32) */
  mpz_mul_2exp(n, n, 32);                   /* n <<= 32 */
  mpz_add_ui(n, n, (unsigned int)ull);      /* n += (unsigned int)ull */
}

unsigned long long mpz_get_ull(mpz_t n) {
  unsigned int lo, hi;
  mpz_t tmp;

  mpz_init(tmp);
  mpz_mod_2exp(tmp, n, 64); /* tmp = (lower 64 bits of n) */

  lo = mpz_get_ui(tmp);       /* lo = tmp & 0xffffffff */
  mpz_div_2exp(tmp, tmp, 32); /* tmp >>= 32 */
  hi = mpz_get_ui(tmp);       /* hi = tmp & 0xffffffff */

  mpz_clear(tmp);

  return (((unsigned long long)hi) << 32) + lo;
}

void search() {
  puts("search");
  std::vector<std::thread> threads;
  uint32_t batch_size = m / thread_num + thread_num;
  for (uint32_t i = 0; i < thread_num; ++i) {
    threads.emplace_back(hash_thread, i * batch_size,
                         std::min(m, (i + 1) * batch_size));
  }

  for (auto &thread : threads) {
    thread.join();
  }
}
void init() {
  mpz_init(mod);
  mpz_init(n64);
  mpz_init(one);
  mpz_init(n);
  mpz_init(e);
  mpz_init(c);
  mpz_set_ui(one, 1);
  mpz_set_ui(mod, 1u);
  mpz_mul_2exp(mod, mod, 64);
  mpz_set_ull(n64, N);
  mpz_mod(n64, n64, mod);
  mpz_set_str(n,
              "4839012640069462694052839372182629440212055100338241404301204069"
              "6542220894278174261030046277223745048983509252576444702682791530"
              "5166372385721345243437217652055280011968958645513779764522873874"
              "8761689984295465231814046527574741479675188564394393146194024477"
              "0334513946031776474305522700959547794931559133410262366461661684"
              "2043021518775210997349987012692811620258928276654394316710846752"
              "7320084800881493951450191593975924156370143907137980321250109695"
              "9733589339902211490667999698214756624524421252482434664529763742"
              "5927685406944205604775116409108280942928854694743108774892001745"
              "535921521172975113294131711065606768927",
              10);
  mpz_set_str(e, "65537", 10);
  mpz_set_str(c,
              "3208816986622427261221526595760604965389214099768955828750899537"
              "0514484169196334366565127648048579566755782513043246645568492131"
              "4043200553005547236066163215094843668681362420498455007509549517"
              "2132854537731024815743908645749502594797656628441025536529770000"
              "3576929560656672275294929778164628926234162354941437626247090874"
              "9643200171565760656987980763971637167709961003784180963669498213"
              "3696516806781499625122164484006816544105367086612065948365971260"
              "1219281351979752608208296961691580629911466603794371843564479666"
              "8877715954887614703727461595073689441920573791980162741306838415"
              "524808171520369350830683150672985523901",
              10);
}
int main() {
  init();
  puts("init success");
  search();
}
