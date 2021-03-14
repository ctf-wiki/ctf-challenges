pragma solidity ^0.4.8;
contract Owned {
    address public owner;

    function Owned() public {
        owner = msg.sender;
    }

    modifier onlyOwner {
        require(msg.sender == owner);
        _;
    }

    function transferOwnership(address newOwner) onlyOwner public {
        owner = newOwner;
    }
}

contract DctfChall is Owned {
	uint256 public minbet;
	uint256 public totalinvested;
	uint256 public totalplayers;
	address public bot;

	struct Player {
        address addr;
        uint8 option;
        bytes32 commit;
        bool showed;
        uint256 invested;
    }

	mapping(uint    => Player) internal players;
	mapping(address => uint256) public solvedHistory;
	mapping(address => uint256) public triesHistory;

	function DctfChall(uint256 _minbet, address _bot) public {
		require(_minbet > 0);
		require(_bot != 0x0);

		minbet = _minbet;
		bot   = _bot;
	}

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

	function reveal(uint8 _option, bytes _nonce) 
	onlyWhenPlayed
	isPlaying(msg.sender)
	isValidOption(_option, _nonce)
	public {
		uint p            = getPlayerId(msg.sender);
		players[p].showed = true;
		players[p].option = _option;
	}

	function play() 
	onlyOwner
	public 
	returns (uint8) {
		if(totalplayers < 2) {
			if(totalplayers > 0) {
				if(!players[1].addr.send(players[1].invested)) {
					//shit happens
				}
			}
			reset();
			return 0;
		}

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
		
	function reset() 
	onlyOwner 
	public {
		totalplayers        = 0;
		totalinvested       = 0;
		
		delete players[1];
		delete players[2];
	}

	function getFlag() 
	onlyIfIsPro
	public
	returns (string)
	{
		return 'this guy should receive the reward';
	}


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

	function hasShowed() public returns (bool) {
		return (players[1].showed && players[2].showed);
	}

	function getPlayerId(address _addr) internal returns (uint) {
		if(players[1].addr == msg.sender) {
    		return 1;
    	} 

    	if(players[2].addr == msg.sender) {
    		return 2;
    	}

    	return 0;
    }

	function() public payable { 
		//thanks for the donation
	}

	modifier isPlaying(address player) {
		require(players[1].addr == player || players[2].addr == player);
		_;
	}

	modifier onlyWithBet {
        require(msg.value >= minbet);
        _;
    }

    modifier onlyPlaying {
    	require(totalplayers < 2);
    	_;
    }

    modifier onlyWhenPlayed {
    	require(totalplayers == 2);
    	_;
    }

    modifier isValidOption(uint8 _opt, bytes _nonce) {
    	uint p = getPlayerId(msg.sender);
    	require(p > 0);
    	require(!players[p].showed && keccak256(msg.sender, _opt, _nonce) == players[p].commit);
    	require(_opt >= 1 && _opt <= 5);
    	_;
    }

    modifier onlyIfIsPro() {
    	require(solvedHistory[msg.sender] >= 10 && solvedHistory[msg.sender] == triesHistory[msg.sender]);
    	_;
    }

    modifier onlyValidPlayers() {
    	if(totalplayers == 1) {
    		require(msg.sender != players[totalplayers].addr);
    		require((players[totalplayers].addr == bot && msg.sender != bot) || (players[totalplayers].addr != bot && msg.sender == bot));
    	}
    	_;
    }
}
