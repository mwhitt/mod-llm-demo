# Custom Moderator LLM
This project was built over a weekend to demonstrate the foundational components needed to post-train an LLM with the latest GRPO reasoning techniques. The focus of the LLM's capabilities are on content moderation and flagging content that includes any of the following:  
- Harassment
- Adult content
- Spam
- Non-fiat currency
- Weapon components
- Government services
- Gambling
- IPTV
- Phishing

The LLM is trained with the goal of imporving accuracy and reducing costs.

# Data
Currently the LLM is only tasked with allowing or disallowing content. A future enhancement would be a rating score in each category so that custom rules can be  made more easily.  

**Allowed** eval / train data was scraped from Gumroad listings.  
**Disallowed** eval / train data was synthetically generated. 

## Data Generation
Edit in `main.py` the `generate_allowed_data or generate_disallowed_data` function call to change the root dir. Then run: `make generate_data`.

# Setup Development
Make sure you have uv installed. (https://docs.astral.sh/uv/getting-started/installation/)  

Then call: `make setup`  

# Run LLM Training
Make sure you have a [modal](https://modal.com/) account with a credit card on file. This training should stay under the free monthly credit provided by modal.  

- Setup modal configs locally: `uv run modal setup`  

- Install VSCode `Remote - SSH` extension. 

- Launch modal GPU and establish an ssh tunnel with it by calling: `uv run modal run launch_ssh.py`  

- Call Remote-SSH: Connect to Host

- Locate the modal ip at the end of the output from the launch command. Use this pre-pended with `root@<modal-ip:port>`and enter it in as the host to connect to. The password is `password` set in `launch_ssh.py`.

- Clone this repo into the reomote desktop `https://github.com/mwhitt/mod-llm-demo.git`

- Install `Python` & `Jupyter` extensions 

- Open VSCode terminal on remote machine and type `make train_setup`

- Open notebook `grpo.ipynb` and play the first cell. Follow instructions to connect to a python environment, choose the one in root of project `.venv`

- Continue down the notebook running each cell after the other until training is completed.  


This notebook was based on [Unsloth Llama 3.1 8B GRPO](https://colab.research.google.com/github/unslothai/notebooks/blob/main/nb/Llama3.1_(8B)-GRPO.ipynb#scrollTo=ptqkXK2D4d6p).  

To monitor the GPU memory and usage you can type `watch -n0.1 nvidia-smi` in the VSCode terminal. 

# TODO

- [ ] Improve data quality, diversity and add ratings for each category.
- [ ] Optimize prompts and tuning parameters.
- [ ] Update rewards system to better reflect moderation goals.
- [ ] Add better observability into training.
- [ ] Once improvements have been made, increase training time to maximize reinforcement learning. 