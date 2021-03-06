# Scripts and Wiki for Azure

![](docs/azure_logo.png)

## First steps
1. Install Azure CLI 2.0 (tested with 2.0.29):
https://docs.microsoft.com/en-us/cli/azure/install-azure-cli

2. Authenticate with `az login` in command line using your student credentials:
    - ФТиАД: e-mail address with invitation from Sberbank
    - ПМИ: student*@zimovnovgmail.onmicrosoft.com

3. Authenticate in http://portal.azure.com (Google Chrome is recommended) using the same credentials.

4. Install Python 2 or 3

5. `pip install joblib` or `pip3 install joblib` based on your Python version

6. If you use Windows, install Putty for ssh: https://www.putty.org/

7. If you use Windows, install https://git-scm.com/

## How-To's
1. Clone this repo running: `git clone https://github.com/ZEMUSHKA/lsml_hse`
2. Switch to azure subscription we use if you've used azure before:
- ФТиАД: `az account set --subscription "8a6f80b4-e575-43c3-94ee-bab031dd0042"`
- ПМИ: `az account set --subscription "Sponsorship 2017"`
3. Use any of the below:

[How to create a Hadoop cluster](docs/CREATE_CLUSTER.md)

[How to create a machine with GPU](docs/CREATE_GPU.md)

[Admin notes](docs/ADMIN.md)
