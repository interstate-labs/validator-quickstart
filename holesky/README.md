## Interstate

Interstate is a proposer commitment network that sits on top of Flashbots / MEV Boost. Please view docs.interstate.so/research for details on the protocol.

We are a sidecar that auctions off the transaction inclusion rights to users that seek to buy preconfirmations, and apps that seek to buy blockspace for blockspace futures.

Have an ethereum validator running and run our sidecar as well to begin earning rewards.

## If you are already running an eth validator, start the sidecar

1. Update `cb-config.toml` file (for commit-boost)
2. Update `.config` file (for interstate-sidecar)
3. Run the interstate-sidecar and commit-boost: ```docker compose up```


Congrats, You're finished with the setup! 


If you're not running a validator read [here](https://github.com/interstate-labs/validator-quickstart-dev/blob/main/holesky/Start_New_Validator.md)

