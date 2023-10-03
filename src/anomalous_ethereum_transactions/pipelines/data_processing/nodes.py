"""
This is a boilerplate pipeline 'data_processing'
generated using Kedro 0.18.13
"""

import logging
import pandas as pd
from web3 import Web3
from kedro.config import ConfigLoader


def get_block_data(block_number, infura_API_key):
    """Retreive transactions data by block using infura

    Args:
        block_number: block of interest
        infura_API_key: infura API key (stored inside the local conf (conf/local/parameters_data_processing.yml))

    Returns:
        dataframe with all the transactions of this block (keep only numerical fields and hash)
    """

    # Connect to Infura using an Infura API key
    infura_url = "https://mainnet.infura.io/v3/"+infura_API_key
    web3 = Web3(Web3.HTTPProvider(infura_url))

    # Retrieve block data for the given block number
    block = web3.eth.get_block(block_number)
    transactions_l = []
    gasUsed_l = []
    for tx_hash in block['transactions']:
        tx = web3.eth.get_transaction(tx_hash)
        transactions_l.append(tx)
        receipt = web3.eth.get_transaction_receipt(tx_hash)
        if receipt:
            # Get the gas used from the receipt
            gas_used = receipt['gasUsed']
        else :
            gas_used = float("nan")
        gasUsed_l.append(gas_used)
    transactions_df = pd.DataFrame(transactions_l)
    transactions_df['gasUsed'] = gasUsed_l
    transactions_df['transactionRank'] = transactions_df.transactionIndex/transactions_df.transactionIndex.max()
    # Return the block data
    return transactions_df


def get_blocks_data(block_number_start, block_number_end, infura_API_key):
    """Retreive transactions data for a list of blocks using infura
    (from block_number_start to block_number_end included)

    Args:
        block_number_start: number of the starting block
        block_number_end: number of the ending block (included)
        infura_API_key: infura API key (stored inside the local conf (conf/local/parameters_data_processing.yml))

    Returns:
        _description_
    """

    logger = logging.getLogger(__name__)
    logger.info("Starting to source on-chain data from block %i to block %i.", block_number_start, block_number_end)
    tx_df = pd.DataFrame()
    for block_number in range(block_number_start, block_number_end+1):
        logger.info("Sourcing on-chain data for block %i...", block_number)
        tx_df = pd.concat([tx_df,get_block_data(block_number, infura_API_key)])

    tx_df.hash = tx_df.hash.apply(lambda x: x.hex())
    tx_df.index = tx_df.hash
    tx_df.index.name=None
    colToKeep_v = ["hash","blockNumber","gas","gasUsed","gasPrice","maxFeePerGas","maxPriorityFeePerGas","nonce","transactionIndex","type","value","transactionRank"]
    filter_tx_df = tx_df[colToKeep_v].copy()
    filter_tx_df['transactionPrice'] = filter_tx_df.gasPrice*filter_tx_df.gasUsed
    return filter_tx_df
        