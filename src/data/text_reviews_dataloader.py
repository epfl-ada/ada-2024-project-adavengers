import pandas as pd
from torch.utils.data import DataLoader, Dataset, random_split


class TextReviews(Dataset):
    """
    Dataset class for text reviews that are stored in a pandas DataFrame (which has been computed by another script with all preprocessing steps/cleaning/merging done)
    """

    def __init__(self, path_to_df):
        """
        Init the Dataset from the dataframe
        @param path_to_df: path to the pickle file containing the dataframe
        """
        super().__init__()
        self.df = pd.read_csv(path_to_df)

    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):
        return self.df['text'].iloc[idx]


class TextReviewDataLoader(DataLoader):
    """
    Allows to sample train/val/test data from the text reviews dataset
    """

    def __init__(self, text_dataset: TextReviews, batch_size: int = 32, train_ratio: float = 0.8, val_ratio: float = 0.1,
                 test_ratio: float = 0.1) -> None:
        """
        Initialize a dataloader for each of the train, val and test datasets
        @param text_dataset: dataset containing all the text reviews
        @param batch_size: batch size for the dataloader
        @param train_ratio: training set % of the dataset
        @param val_ratio: validation set % of the dataset
        @param test_ratio: test set % of the dataset
        """
        assert train_ratio + val_ratio + test_ratio == 1, "The sum of train_ratio, val_ratio and test_ratio should be equal to 1"
        total_items = len(text_dataset)

        train_size = int(total_items * train_ratio)
        val_size = int(total_items * val_ratio)
        test_size = total_items - train_size - val_size

        self.train_dataset, self.val_dataset, self.test_dataset = random_split(text_dataset, [train_size, val_size, test_size])
        self.batch_size = batch_size

    def train_dataloader(self):
        return DataLoader(self.train_dataset, batch_size=self.batch_size, shuffle=True)

    def val_dataloader(self):
        return DataLoader(self.val_dataset, batch_size=self.batch_size, shuffle=False)

    def test_dataloader(self):
        return DataLoader(self.test_dataset, batch_size=self.batch_size, shuffle=False)
