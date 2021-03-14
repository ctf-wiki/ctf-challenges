#include <eosio/eosio.hpp>
#include <eosio/system.hpp>

using namespace eosio;

class [[eosio::contract]] easyeos : public contract {
  private:
    struct [[eosio::table]] user_info {
      name username;
      uint32_t win;
      uint32_t lost;
      auto primary_key() const { return username.value; }
    };

    struct [[eosio::table]] seed {
      uint64_t        key = 1;
      uint32_t        value = 1;

      auto primary_key() const { return key; }
    };

    struct [[eosio::table]] mail {
      name username;
      std::string address;
      auto primary_key() const { return username.value; }
    };

    typedef eosio::multi_index<name("users"), user_info> users_table;
    typedef eosio::multi_index<name("seed"), seed> seed_table;
    typedef eosio::multi_index<name("mails"), mail> mails_table;

    users_table _users;
    seed_table _seed;
    mails_table _mails;

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
    
    // Store the updated seed value in the table
    _seed.modify( seed_iterator, _self, [&]( auto& s ) {
      s.value = new_seed_value;
    });
    
    // Get the random result in desired range
    int random_result = new_seed_value % range;
    return random_result;
    }

  public:
    using contract::contract;
    easyeos( name receiver, name code, datastream<const char*> ds ):contract(receiver, code, ds),
                       _users(receiver, receiver.value),
                       _seed(receiver, receiver.value),
                       _mails(receiver, receiver.value) {}
    
    [[eosio::action]]
    void bet( name username, int num)
    {
      // Ensure this action is authorized by the player
      require_auth(username);
      int random_num = random(5);
      
      // Create a record in the table if the player doesn't exist
      auto user_iterator = _users.find(username.value);
      if (user_iterator == _users.end()) {
        user_iterator = _users.emplace(username,  [&](auto& new_user) {
        new_user.username = username;
        });
      }

      check(user_iterator->lost <= 0, "You lose!");

      if(num == random_num){
        _users.modify(user_iterator, username, [&](auto& new_user) {
          new_user.win = user_iterator->win + 1;
        });
      }
      else{
        _users.modify(user_iterator, username, [&](auto& new_user) {
          new_user.lost = 1;
        });
      }
      
      // print( "Bet, ", username,",num = ", num, ", random = ", random_num, ", win = ", user_iterator->win, " , lost = ", user_iterator->lost);
    }

    [[eosio::action]]
    void sendmail(name username, std::string address){
      require_auth(username);
      // Create a record in the table if the player doesn't exist
      auto user_iterator = _users.find(username.value);
      if (user_iterator == _users.end()) {
        user_iterator = _users.emplace(username,  [&](auto& new_user) {
        new_user.username = username;
        });
      }
      check(user_iterator->win >= 10, "You need to win at least 10 times.");

      print("You win!!! Email: ", address);
      auto mail_iterator = _mails.find(username.value);
      if (mail_iterator == _mails.end()) {
        mail_iterator = _mails.emplace(username,  [&](auto& new_mail) {
          new_mail.username = username;
          new_mail.address = address;
        });
      }
      else{
        _mails.modify(mail_iterator, username, [&](auto& new_mail) {
          new_mail.address = address;
        });
      }
    }
};

