# Import os for managing file saving paths
import os
import matplotlib.pyplot as plt
import seaborn as sns
import config

#set clean default theme for plots
sns.set_theme(style="whitegrid")


#function to create correlation heatmap
def plot_risk_heatmap(df):
    #list of numeric columns to check for correlation
    cols = ['premiumRate', 'indemnityLevel', 'sumInsured', 'TGP']
    valid_cols = []

    #simple for loop to check which columns exist in DataFrame
    for c in cols:
        if c in df.columns:
            valid_cols.append(c)

    #check if we have at least 2 valid numeric columns
    if len(valid_cols) >= 2:
        plt.figure(figsize=(8, 6))
        #calculate correlation matrix
        corr_matrix = df[valid_cols].corr()

        #plot correlation heatmap
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
        plt.title('Risk Profile Correlation Heatmap', fontsize=14, fontweight='bold')
        plt.tight_layout()

        #build file path and save PNG image
        save_path = os.path.join(config.OUTPUT_DIR, 'risk_heatmap.png')
        plt.savefig(save_path, dpi=300)
        plt.close()
        print("Saved:", save_path)


#function to create stacked bar chart for government shares
def plot_fiscal_share_stacked(df):
    group_cols = ['farmerShareValue', 'stateShareValue', 'goiShareValue']

    #check if crop_year and share columns exist
    if 'crop_year' in df.columns:
        if 'farmerShareValue' in df.columns:
            #group data by crop year and sum share values
            yearly_shares = df.groupby('crop_year')[group_cols].sum()

            #calculate percentages adding up to 100%
            yearly_proportions = yearly_shares.div(yearly_shares.sum(axis=1), axis=0) * 100

            #plot stacked bar chart
            ax = yearly_proportions.plot(kind='bar', stacked=True, figsize=(10, 6), colormap='Accent')
            plt.title('Fiscal Share Composition Across Years (%)', fontsize=14, fontweight='bold')
            plt.xlabel('Crop Year')
            plt.ylabel('Percentage Share (%)')
            plt.legend(['Farmer Share', 'State Share', 'GOI Share'], loc='lower right')
            plt.xticks(rotation=0)
            plt.tight_layout()

            #save PNG image to output directory
            save_path = os.path.join(config.OUTPUT_DIR, 'fiscal_share_stacked.png')
            plt.savefig(save_path, dpi=300)
            plt.close()
            print("Saved:", save_path)


#function to create boxplot for insurance providers
def plot_provider_indemnity_boxplot(df):
    #check if company name and indemnity level exist
    if 'insuranceCompanyName' in df.columns:
        if 'indemnityLevel' in df.columns:
            plt.figure(figsize=(12, 6))

            #plot boxplot showing indemnity distributions
            sns.boxplot(data=df, x='insuranceCompanyName', y='indemnityLevel', palette='Set3')
            plt.title('Indemnity Level Distribution by Insurance Company', fontsize=14, fontweight='bold')
            plt.xlabel('Insurance Company')
            plt.ylabel('Indemnity Level (%)')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()

            #save PNG image to output directory
            save_path = os.path.join(config.OUTPUT_DIR, 'provider_indemnity_boxplot.png')
            plt.savefig(save_path, dpi=300)
            plt.close()
            print("Saved:", save_path)


#function to create line plot for total sum insured over time
def plot_temporal_sum_insured(df):
    #check if required columns exist
    if 'crop_year' in df.columns:
        if 'sumInsured' in df.columns:
            if 'season_name' in df.columns:
                plt.figure(figsize=(10, 6))

                #plot seasonal trend line chart
                sns.lineplot(
                    data=df,
                    x='crop_year',
                    y='sumInsured',
                    hue='season_name',
                    marker='o',
                    estimator='sum',
                    errorbar=None
                )
                plt.title('Temporal Sum Insured Trajectory by Season', fontsize=14, fontweight='bold')
                plt.xlabel('Crop Year')
                plt.ylabel('Total Sum Insured (INR)')
                plt.tight_layout()

                #save PNG image to output directory
                save_path = os.path.join(config.OUTPUT_DIR, 'temporal_sum_insured.png')
                plt.savefig(save_path, dpi=300)
                plt.close()
                print("Saved:", save_path)


#master function executing all plot functions
def generate_all_plots(df):
    print("\nGenerating Exploratory Data Visualizations...")
    plot_risk_heatmap(df)
    plot_fiscal_share_stacked(df)
    plot_provider_indemnity_boxplot(df)
    plot_temporal_sum_insured(df)
    print("All Data Visualizations Exported Successfully!")