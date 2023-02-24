# turtles-feb-2023

Last month's turtles challenge can be found [here](https://github.com/spr-networks/turtles-january-23)

## Rules 
1. Submit writeups by e-mail to turtles@supernetworks.org
2. The best writeup along with the first two writeups (that are correct) will be awarded pis as prizes. Writeups should include functional exploits/scripts.

## How to play

This is a self hosted challenge -- your goal is to collect 6 flags. 

You can either run the containers here or play along in your web browser at [https://turtles.supernetworks.org](https://turtles.supernetworks.org)

## Dependencies
See host-install.sh. Make sure wireless-regdb is installed on the host, along with the mac hwsim drivers. It was observed that missing the regulatory db on the host stops the challenges from running correctly.

## Running the system
```
docker-compose up -d
sudo ./setup.sh

docker exec -it t1_start bash or ssh root@localhost -p 2222 (password is mutant_n1nj4_turtle)
```
