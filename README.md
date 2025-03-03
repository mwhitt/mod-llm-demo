# Custom Moderator LLM

This project was built over a weekend to demonstrate the foundational components needed to post-train an LLM with the latest GRPO reasoning techniques. The LLM focuses on content moderation and flagging content that includes any of the following:
- Harassment
- Adult content
- Spam
- Non-fiat currency
- Weapon components
- Government services
- Gambling
- IPTV
- Phishing

The LLM is trained with the goal of improving accuracy and reducing costs.

# Data

Currently, the LLM is only tasked with allowing or disallowing content. A future enhancement would be a rating score in each category so that custom rules can be made more easily.

**Allowed** eval/train data was scraped from Gumroad listings.  
**Disallowed** eval/train data was synthetically generated.

## Data Generation

Edit the `generate_allowed_data` or `generate_disallowed_data` function call in `main.py` to change the root directory. Then run: `make generate_data`.

# Development Setup

Make sure you have uv installed. (https://docs.astral.sh/uv/getting-started/installation/)

Then call: `make setup`

# LLM Training

Make sure you have a [modal](https://modal.com/) account with a credit card on file. This training should stay under the free monthly credit provided by Modal.

- Setup Modal configs locally: `uv run modal setup`

- Install VSCode `Remote - SSH` extension.

- Launch Modal GPU and establish an SSH tunnel by calling: `uv run modal run launch_ssh.py`

- In VSCode, select Remote-SSH: Connect to Host

- Locate the Modal IP at the end of the output from the launch command. Enter `root@<modal-ip:port>` as the host to connect to. The password is `password` as set in `launch_ssh.py`.

- Clone this repo into the remote desktop: `git clone https://github.com/mwhitt/mod-llm-demo.git`

- Install `Python` & `Jupyter` extensions

- Open VSCode terminal on the remote machine and type `make train_setup`

- Open notebook `grpo.ipynb` and run the first cell. Follow instructions to connect to a Python environment, choosing the one in the root of the project (`.venv`)

- Run each cell in the notebook sequentially until training is completed.

This notebook was based on [Unsloth Llama 3.1 8B GRPO](https://colab.research.google.com/github/unslothai/notebooks/blob/main/nb/Llama3.1_(8B)-GRPO.ipynb#scrollTo=ptqkXK2D4d6p).

To monitor GPU memory and usage, type `watch -n0.1 nvidia-smi` in the VSCode terminal.

# Inference
To run the model locally: `make serve`  

Use your model uploaded to Hugging Face on the final cell in the notebook then change the value in the Makefile serve command.

# Evals
Comming Soon...

# TODO

- [ ] Improve data quality, diversity and add ratings for each category
- [ ] Optimize prompts and tuning parameters
- [ ] Update rewards system to better reflect moderation goals
- [ ] Add better observability into training
- [ ] Once improvements have been made, increase training time to maximize reinforcement learning
- [ ] Deploy model in test / production environment. 