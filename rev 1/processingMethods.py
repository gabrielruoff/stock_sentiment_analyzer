
class processingMethods:

    def __init__(self):
        pass

    # display the percentage of instances where this stocks opens low and closes high in
    # passed dataframe's interval
    def simpleOLCHStatistics(self, data):

        OLCH_count = 0
        row_count = 0

        ticker = list(data)[0][0]

        # compare open/close prices and add to count if applicable
        for index, row in data.iterrows():
            print("row", row)
            row_count += 1

            if row[(ticker, 'Open')] > row[(ticker, 'Close')]:
                OLCH_count += 1

        # return number of OLCH's and percentage
        return [OLCH_count, OLCH_count / row_count]
