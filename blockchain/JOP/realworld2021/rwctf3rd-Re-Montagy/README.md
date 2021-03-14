RealWorldCTF 3rd Finals - Re:Montagy
-----------------------

### Challenge
#### Background:

Hi there, I heard from my agent that many people ´\_>\` solved my challenge last year which was joyful.
You might notice something when seeing this challenge name. And yes, last year's challenge was actually a part of this final art.
A game started a year ago, lost between 0&1, come from the path and back through the shadow, will you catch the 'Montage' spirit?
I'm waiting for you, from the past to the future.

-- A. Monica

#### Description:

$ nc <docker_ip> 10101

#### provided files:

- Montagy.sol: the target contract
- Puzzle.sol: the contract deployed during newPuzzle

#### Goal:

Let the ETH balance of Montagy contract becomes 0.

### Deployment
```
$ cd deploy
$ docker build -t rwctf3rd-re-montagy .
$ docker run -d --rm -p 0.0.0.0:10101:10101 --name=chal1 -e TERM=xterm rwctf3rd-re-montagy
$ nc localhost 10101
```
or
```
$ docker pull xhyumiracle/rwctf3rd-re-montagy
```

### Info
https://ctftime.org/task/14505
