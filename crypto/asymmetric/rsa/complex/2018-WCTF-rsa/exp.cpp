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
constexpr const size_t thread_num = 8;

constexpr const uint64_t N = 13677534082369767711uLL;
mpz_t mod, n64,one;

struct __attribute__((packed)) Candidate {
  uint64_t p;
  uint32_t t;
  bool operator<(const Candidate &rhs) const { return p < rhs.p; }
};

Candidate *candidates;
uint8_t *bitvec;
constexpr const size_t bitvec_size = 1u << 29u;
std::mutex io_mtx;

void save_candidates() {
  FILE *f = fopen("candidates.bin", "wb");
  fwrite(candidates, sizeof(Candidate), m, f);
  fclose(f);
}

void load_candidates() {
  FILE *f = fopen("candidates.bin", "rb");
  fread(candidates, sizeof(Candidate), m, f);
  fclose(f);
}

void hash_thread(uint32_t lo, uint32_t hi) {
  uint32_t buf[9];
  uint8_t digest[64];
  std::copy(nums, nums + 8, buf);

  for (uint32_t i = lo; i < hi; ++i) {
    if ((i & 0xffffff) == 0) {
      std::lock_guard<std::mutex> l(io_mtx);
      printf("hash %x\n", i);
    }

    buf[8] = i;
    SHA512((uint8_t *)buf, 36, digest);

    auto &c = candidates[i];
    c.t = i;
    c.p = __builtin_bswap64(*(uint64_t *)&digest[56]); // big endian!
  }
}

void generate_candidates() {
  puts("generate");
  std::vector<std::thread> threads;
  uint32_t batch_size = m / thread_num + thread_num;
  for (uint32_t i = 0; i < thread_num; ++i) {
    threads.emplace_back(hash_thread, i * batch_size,
                         std::min(m, (i + 1) * batch_size));
  }

  for (auto &thread : threads) {
    thread.join();
  }

  puts("sort");
  std::sort(candidates, candidates + m);

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

uint32_t find_candidate(uint64_t p) {
  size_t lo = 0, hi = m - 1;
  while (lo <= hi) {
    auto mid = (lo + hi) / 2;
    auto &c = candidates[mid];
    if (c.p < p) {
      lo = mid + 1;
    } else if (c.p > p) {
      hi = mid - 1;
    } else {
      return c.t;
    }
  }
  return m;
}

bool check_candindate(const Candidate &c) {
  mpz_t d, invd,g;
  uint64_t tmp;

  mpz_init(d);
  mpz_init(invd);
  mpz_init(g);

  mpz_set_ull(d, c.p);
  mpz_gcd(g,d,mod);
  if (mpz_cmp(g,one)!=0){
    mpz_clear(d);
    mpz_clear(invd);
    mpz_clear(g);
    return false;
  }
  //printf("%llx\n",c.p);
  mpz_invert(invd, d, mod);
  mpz_mul(invd, invd, n64);
  mpz_mod(invd, invd, mod);
  tmp = mpz_get_ull(invd);
  auto i = find_candidate(tmp);
  mpz_clear(d);
  mpz_clear(invd);
  mpz_clear(g);
  if (i < m) {
    std::lock_guard<std::mutex> l(io_mtx);
    printf("b64: %llx idx_b: %u idx_d: %u\n", c.p, c.t,
           i); // later reconstruct all 512 bits of p and q from the t values
    return true;
  }
  return false;
}



void search_thread(uint32_t lo, uint32_t hi) {
  for (uint32_t i = lo; i < hi; ++i) {
    if ((i & 0xffffff) == 0) {
      std::lock_guard<std::mutex> l(io_mtx);
      printf("search %x\n", i);
    }

    check_candindate(candidates[i]);
  }
}

void search() {
  puts("search");
  std::vector<std::thread> threads;
  uint32_t batch_size = m / thread_num + thread_num;
  for (uint32_t i = 0; i < thread_num; ++i) {
    threads.emplace_back(search_thread, i * batch_size,
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
  mpz_set_ui(one,1);
  mpz_set_ui(mod, 1u);
  mpz_mul_2exp(mod, mod, 64);
  mpz_set_ull(n64, N);
  mpz_mod(n64, n64, mod);
}
int main() {
  candidates = new Candidate[m];
  init();
  puts("init success");
  //generate_candidates();
  //save_candidates();
  load_candidates();
  puts("load success");
  search();
}
