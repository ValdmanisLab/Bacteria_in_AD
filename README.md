# Custom Scripts for our manuscript
Here we provide 3 custom scripts for your use in evaluating our manuscript and processing genomic data.

### 1. A script for downloading regions from binary alignment files from s3 storage when you must use a pre-signed url and key for download.
### 2. A python script for filtering binary alignment files for reads with gaps of a certain length.
   While we cannot provide the sn-RNA seq that we used, there are many datasets available which will demonstrate this.
   One RNA-seq dataset which you may test it on if you like can be downloaded here:
   
   `wget https://www.encodeproject.org/files/ENCFF802TLC/@@download/ENCFF802TLC.bam`

   We tested this script on the following platform and package versions. It should happily run on unix system:  
   OS: WSL2 Ubuntu 22.04  
   Python       3.11.4  
   pip          23.2.1  
   pysam        0.22.1  
   numpy        1.26.4  
   samtools     1.1  
   You may install the python dependencies with this command: `pip3 install pysam numpy`  
   Dependency install and using the script should take <1min on .bam files trimmed to a region 40kb or less.

   #### Demo to run it on the RNA-seq dataset that we have attached, you may do the following:
   a. create a directory on an terminal with python installed  
   c. ensure that you have the python dependencies using `pip3 install pysam numpy`  
   d. ensure that you have samtools, either via a conda environment or installed directly with your native package manager, such as through apt: `sudo apt install samtools`  
   e. run the following code chunk to ensure to download the example rnaseq dataset. Please give it at least 5 minutes to download the .bam.  
   `wget https://www.encodeproject.org/files/ENCFF802TLC/@@download/ENCFF802TLC.bam -O ENCFF802TLC.bam && \  `   
   `samtools index ENCFF802TLC.bam && \  `   
   `samtools view -b ENCFF802TLC.bam chr19:44890796-44924393 -o ENCFF802TLC_chr19_region.bam && \  `  
   `rm ENCFF802TLC.bam`  
   f. download the gap.py script and run it with `python3 gap.py`  
   g. drop the resultant .bam sitting in the new ENCFF802TLC_chr19_region directory into IGV to visualize.

Expected output, when you put in APOE for the coordinates in IGV:
<img width="1061" height="215" alt="image" src="https://github.com/user-attachments/assets/e23a2051-aad7-4ad7-8a44-fd4a335497ab" />

   
### 3. A script for analyzing the relationship between dementia and infections on the All Of Us Controlled tier.  
   Our analysis requires access to the Controlled Tier of AllOfUs, which individuals at many institions can register for access to here:  
   https://www.researchallofus.org/register/  
   Package version information can be found here: https://web.archive.org/web/20250710192917/https://support.researchallofus.org/hc/en-us/articles/6736634017428-Pre-installed-tools-on-Researcher-Workbench






# Further details on Analysis of Dementia and Infections in ALL OF US 

## 1. Purpose of the Analysis
- Investigate temporal patterns and correlations between infections and their association with dementia and Alzheimer's disease.
- Use SQL to extract relevant data from the electronic health records (EHR) and perform enrichment analysis inside the ALL OF US database.
- The script should be pasted into an jupyter notebook after spinning up a jupyter instance in a workspace dedicated to the task.

## 2. Environment Setup
- **Goal**: Prepare the necessary tools and libraries for data extraction, transformation, and analysis.
- **Key Steps**:
    - Validate the environment by listing Python and Conda packages.
    - Import essential libraries:
        - **Data manipulation**: `pandas`, `numpy`
        - **Statistical analysis**: `scipy`, `statsmodels`
        - **Visualization**: `matplotlib`, `seaborn`
        - **Domain-specific tools**: `hail`, `lifelines`

## 3. Data Extraction
- **Source**: SQL database containing patient EHRs from the ALL OF US database.
- **Focus**:
    - Extract patient IDs, diagnosis dates for bacterial infections, retroviruses, dementia, and Alzheimer's disease.
    - Ensure data completeness and consistency.

## 4. Data Processing
- **Transformations**:
    - Convert timestamps into comparable formats.
    - Sort events chronologically to establish order (e.g., bacterial infections preceding retrovirus or vice versa).
- **Data Cleaning**:
    - Handle missing or outlier data.
    - Remove duplicates or irrelevant entries.
    - Perform checks and cleaning for the **sex at birth** field.
    - Keep patients that meet the following criteria:
        - At least **60 years old** (CDR version 7).
        - At least **10 EHR entries**.
        - Valid information about **age** and **sex at birth**.

## 5. Statistical Analysis
### Tests Applied
- **Enrichment Analysis**:
    - **Question**: If you have a specific disease (e.g., bacterial infection), are you more likely to also have dementia/Alzheimer's (AD)?
    - **Contingency Table Construction**:
        - `a`: Number of individuals who have both the specific disease (`disease=1`) and dementia/Alzheimer's (`dementia_alzheimer=1`).
        - `b`: Number of individuals who have the specific disease (`disease=1`) but do not have dementia/Alzheimer's (`dementia_alzheimer=0`).
        - `c`: Number of individuals who do not have the specific disease (`disease=0`) but do have dementia/Alzheimer's (`dementia_alzheimer=1`).
        - `d`: Number of individuals who have neither the specific disease (`disease=0`) nor dementia/Alzheimer's (`dementia_alzheimer=0`).
    - **Purpose**: Evaluate whether having a disease is associated with an increased likelihood of also having dementia/Alzheimer's (AD).
- **Violin Plots**:
    - **T-Test**: Test if the median age difference between AD and disease onset is significantly different from zero, indicating a timing difference (e.g., disease first vs. dementia first).
    - **Direction Test**: Determine whether the disease is more likely to occur before AD (First Disease), after AD (First AD), or at the same time.
- **Group Comparisons**:
    - **One-Way ANOVA**:
        - Compare means across multiple groups (e.g., dementia/Alzheimer's vs. infections).
        - Assumptions: Normality and homogeneity of variance.
        - Follow-up: Conduct post hoc tests (e.g., Tukey’s HSD) for significant results.
    - **Mann-Whitney U Test**:
        - Compare two independent groups when data does not meet normality assumptions (e.g., age at dementia/AD onset vs. age at infection).
- **Time-to-Event Analysis**:
    - **Kaplan-Meier Survival Analysis**:
        - Evaluate the time to disease onset (e.g., from bacterial infection to dementia/Alzheimer’s diagnosis).
        - Outputs: Survival curves with log-rank tests for group comparison.
    - Compare survival curves for:
        - Patients with AD/Dementia vs. those without bacterial infections and,
        - Groups with AD/Dementia 1, 2, 3, or more infections.
- **Categorical Data Analysis**:
    - **Enrichment Analysis**:
        - Identify enrichment of Dementia/Alzheimer's in patients with bacterial infections.
        - **Statistical Tests**: Fisher’s Exact Test
- **Key Metrics**:
    - Odds ratios, p-values, confidence intervals.

## 6. Visualization
- **Tools**: Use bar charts, scatter plots, Kaplan-Meier survival curves, histograms, KDE plots, pie charts, and violin plots to summarize findings visually.

### What is KDE (Kernel Density Estimation)?
- **KDE** stands for Kernel Density Estimation.
- It is a statistical method used to estimate the **probability density function (PDF)** of a random variable based on a finite data sample.
- KDE is used to create a **smooth curve** (density function) that represents the underlying distribution of the data.
- **Advantages**:
    - Unlike histograms, which are discrete, KDE provides a **continuous representation** of the data.
- **Kernel**:
    - The "kernel" is a mathematical function used to smooth the data points.
    - **Gaussian kernels** (bell-shaped) are the most commonly used, though others exist.
- **Purpose in This Study**:
    - KDE plots were used to visualize the distribution of ages or other continuous variables to better understand trends in the dataset, without showing summary data from counts less than 20.

## 7. Findings
- Identify significant temporal and statistical patterns linking bacterial infections and neurological conditions.
- Discuss potential causal or correlative relationships.

---

### Additional Details:
- For the **Kaplan-Meier plots**:
    - The **log-rank test** is used to compare survival curves between two groups:
        - Null Hypothesis (H₀): The survival distributions of the two groups are the same.
        - Alternative Hypothesis (H₁): The survival distributions of the two groups are different.
    - Compare the survival experiences of:
        - Patients with AD/Dementia and no infection.
        - Patients with AD/Dementia and 1, 2, 3, or more infections.
- For the **enrichment analysis**:
    - Evaluate whether having a disease increases the likelihood of also having Alzheimer's disease or Dementia.


# License

Copyright (c) 2024 Evangelos Nizamis, Eli Kaufman, Paul Valdmanis

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

1. The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
2. THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

If you use this software in your work or research, we kindly request that you acknowledge its use by citing the following reference:  
[https://github.com/ValdmanisLab/Bacteria_in_AD](https://github.com/ValdmanisLab/Bacteria_in_AD).
