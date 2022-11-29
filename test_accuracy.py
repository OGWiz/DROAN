import pandas as pd
from tkinter import *
from pandastable import Table, config

class TableApp(Frame):
        """Basic test frame for the table"""
        def __init__(self, df, parent=None):
            self.parent = parent
            Frame.__init__(self)
            self.main = self.master
            self.main.geometry('2560x1600')
            self.main.title('Results')
            f = Frame(self.main)
            f.pack(fill=BOTH,expand=1)
            self.table = pt = Table(f, dataframe=df,
                                    showtoolbar=True, showstatusbar=True)
            options = {'floatprecision': 10}
            config.apply_options(options, pt)
            pt.show()
            return

if __name__ == '__main__':
    df = pd.read_csv('outputs/clean_detections.csv')
    del df['Time of Detection']
    del df['Class ID']
    # Size Severity Longitude Latitude 

    df_true = pd.read_csv('outputs/ground_truth.csv')

    # Calculate for TP, FP, FN, TN
    detections = df.values.tolist()    
    ground_truth = df_true.values.tolist()

    TP = 0
    TN = 0
    FP = 0
    FN = 0
    to_remove = []
    new_detections = []
    for detection in detections:
        for truth in ground_truth[:10]:
            if detection[1] == truth[1]:
                if (0.9 * float(truth[2])) < float(detection[2]) < (1.1 * float(truth[2])):
                    if (0.9 * float(truth[3])) < float(detection[3]) < (1.1 * float(truth[3])):
                        if truth not in to_remove:
                            to_remove.append(truth)
                        TP += 1
                        new_detections.append(detection)
                        break
    
    FP = len(detections) - TP

    FN = len(ground_truth) - TP

    try:
        accuracy = ((TN + TP) / (TN + FP + TP + FN))
    except:
        accuracy = 0
    try:
        precision = (TP / (TP + FP))
    except:
        precision = 0
    try:
        recall = (TP / (TP + FN))
    except:
        recall = 0
    try:
        F1_score = (2 * ((precision * recall) / (precision + recall)))
    except:
        F1_score = 0

    final_detections = []
    for dtc in detections:
        if dtc not in new_detections:
            final_detections.append([dtc[0], dtc[1], dtc[2], dtc[3], 'FP'])
        else:
            final_detections.append([dtc[0], dtc[1], dtc[2], dtc[3], 'TP'])

    df_new = pd.DataFrame(final_detections, columns=['Size (m^2)', 'Severity', 'Longitude', 'Latitude', 'Result'])
    
    confusion_matrix = [[' ', ' ', ' ', ' ', ' '], ['True Positives', TP, 'True Negatives', TN, ' '], 
    ['False Positives', FP, 'False Negatives', FN, ' '], ['Accuracy', accuracy, 'Precision', precision, ' '], 
    ['Recall', recall, 'F1-Score', F1_score, ' ']]
    df_confusion_matrix = pd.DataFrame(confusion_matrix, columns=['Size (m^2)', 'Severity', 'Longitude', 'Latitude', 'Result'])

    # Show detected vs true and confusion matrix
    gap = pd.DataFrame([''], columns=[''])
    df_combined = pd.concat([df_new, df_confusion_matrix], axis=0, ignore_index=True)
    df_final = pd.concat([df_combined, gap, df_true], axis=1)
    app = TableApp(df_final)
    #launch the app
    app.mainloop()