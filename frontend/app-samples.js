/* IDCFSS — Sample Dataset Definitions (Minimal Aesthetic) */
const SAMPLES = [
  {
    id: 'titanic', name: 'Titanic Survival',
    tag: 'Classification', rows: 25, cols: 10,
    desc: 'Passenger survival data — missing ages, categorical sex/embarked',
    csv: `PassengerId,Survived,Pclass,Name,Sex,Age,SibSp,Parch,Fare,Embarked
1,0,3,"Braund, Mr. Owen",male,22,1,0,7.25,S
2,1,1,"Cumings, Mrs. John",female,38,1,0,71.28,C
3,1,3,"Heikkinen, Miss. Laina",female,26,0,0,7.93,S
4,1,1,"Futrelle, Mrs. Jacques",female,35,1,0,53.10,S
5,0,3,"Allen, Mr. William",male,35,0,0,8.05,S
6,0,3,"Moran, Mr. James",male,,0,0,8.46,Q
7,0,1,"McCarthy, Mr. Timothy",male,54,0,0,51.86,S
8,0,3,"Palsson, Master. Gosta",male,2,3,1,21.08,S
9,1,3,"Johnson, Mrs. Oscar",female,27,0,2,11.13,S
10,1,2,"Nasser, Mrs. Nicholas",female,14,1,0,30.07,C
11,1,3,"Sandstrom, Miss. Marguerite",female,4,1,1,16.70,S
12,1,1,"Bonnell, Miss. Elizabeth",female,58,0,0,26.55,S
13,0,3,"Saundercock, Mr. William",male,20,0,0,8.05,S
14,0,3,"Andersson, Mr. Anders",male,39,1,5,31.28,S
15,0,3,"Vestrom, Miss. Hulda",female,14,0,0,7.85,S
16,1,2,"Hewlett, Mrs. Mary",female,55,0,0,16.00,S
17,0,3,"Rice, Master. Eugene",male,2,4,1,29.13,Q
18,1,2,"Williams, Mr. Charles",male,,0,0,13.00,S
19,0,3,"Vander Planke, Mrs.",female,31,1,0,18.00,S
20,1,3,"Masselmani, Mrs. Fatima",female,,0,0,7.23,C
21,0,2,"Fynney, Mr. Joseph",male,35,0,0,26.00,S
22,1,2,"Beesley, Mr. Lawrence",male,34,0,0,13.00,S
23,1,3,"McGowan, Miss. Anna",female,15,0,0,8.03,Q
24,1,1,"Sloper, Mr. William",male,28,0,0,35.50,S
25,0,3,"Palsson, Miss. Torborg",female,8,3,1,21.08,S`
  },
  {
    id: 'iris', name: 'Iris Flowers',
    tag: 'Classification', rows: 30, cols: 5,
    desc: 'Classic flower dataset — 3 species, all numeric, clean baseline',
    csv: `sepal_length,sepal_width,petal_length,petal_width,species
5.1,3.5,1.4,0.2,setosa
4.9,3.0,1.4,0.2,setosa
4.7,3.2,1.3,0.2,setosa
4.6,3.1,1.5,0.2,setosa
5.0,3.6,1.4,0.2,setosa
5.4,3.9,1.7,0.4,setosa
4.6,3.4,1.4,0.3,setosa
5.0,3.4,1.5,0.2,setosa
4.4,2.9,1.4,0.2,setosa
4.9,3.1,1.5,0.1,setosa
7.0,3.2,4.7,1.4,versicolor
6.4,3.2,4.5,1.5,versicolor
6.9,3.1,4.9,1.5,versicolor
5.5,2.3,4.0,1.3,versicolor
6.5,2.8,4.6,1.5,versicolor
5.7,2.8,4.5,1.3,versicolor
6.3,3.3,4.7,1.6,versicolor
4.9,2.4,3.3,1.0,versicolor
6.6,2.9,4.6,1.3,versicolor
5.2,2.7,3.9,1.4,versicolor
6.3,3.3,6.0,2.5,virginica
5.8,2.7,5.1,1.9,virginica
7.1,3.0,5.9,2.1,virginica
6.3,2.9,5.6,1.8,virginica
6.5,3.0,5.8,2.2,virginica
7.6,3.0,6.6,2.1,virginica
4.9,2.5,4.5,1.7,virginica
7.3,2.9,6.3,1.8,virginica
6.7,2.5,5.8,1.8,virginica
7.2,3.6,6.1,2.5,virginica`
  },
  {
    id: 'house', name: 'House Prices',
    tag: 'Regression', rows: 30, cols: 8,
    desc: 'Property pricing data — mixed types, missing values, outliers',
    csv: `Id,LotArea,Neighborhood,HouseStyle,YearBuilt,OverallQual,GrLivArea,GarageArea,SalePrice
1,8450,CollgCr,2Story,2003,7,1710,548,208500
2,9600,Veenker,1Story,1976,6,1262,460,181500
3,11250,CollgCr,2Story,2001,7,1786,608,223500
4,9550,Crawfor,2Story,1915,7,1717,642,140000
5,14260,NoRidge,2Story,2000,8,2198,836,250000
6,14115,Mitchel,1Story,1993,5,1362,480,143000
7,10084,Somerst,1Story,2004,8,1694,636,307000
8,10382,NWAmes,2Story,1973,7,2090,484,200000
9,6120,OldTown,1Story,1931,7,1774,468,129900
10,7420,BrkSide,2Story,1939,5,1077,205,118000
11,11200,Sawyer,1Story,1965,5,1040,384,129500
12,11924,SawyerW,2Story,2005,9,2324,736,345000
13,12968,Sawyer,1Story,1962,5,912,352,144000
14,10652,CollgCr,2Story,2006,7,1494,576,279500
15,10920,NAmes,1Story,1960,6,1253,418,157000
16,6120,BrkSide,1Story,1929,6,854,0,132000
17,11241,NAmes,1.5Fin,1970,6,1004,240,149000
18,4426,Sawyer,1Story,1967,4,1296,0,90000
19,11000,Timber,2Story,2004,7,1114,480,159000
20,8400,CollgCr,2Story,2003,5,1339,0,139000
21,8814,SWISU,2Story,1915,8,2102,0,325300
22,7500,OldTown,1Story,1953,6,845,0,139400
23,12579,Sawyer,2Story,1964,5,1445,,230000
24,8370,Timber,2Story,2003,8,1702,514,129900
25,9980,NAmes,1Story,1958,5,,486,154000
26,7281,Mitchel,1Story,1992,,920,420,256300
27,5000,OldTown,2Story,1939,6,1224,0,119900
28,7892,BrkSide,1Story,1948,5,776,194,142125
29,15000,NAmes,1Story,1977,7,1142,382,179900
30,9575,BrkSide,1.5Fin,1920,6,1204,212,129000`
  },
  {
    id: 'diabetes', name: 'Diabetes',
    tag: 'Classification', rows: 30, cols: 9,
    desc: 'Patient health data — outliers in glucose and BMI, binary target',
    csv: `Pregnancies,Glucose,BloodPressure,SkinThickness,Insulin,BMI,DiabetesPedigreeFunction,Age,Outcome
6,148,72,35,0,33.6,0.627,50,1
1,85,66,29,0,26.6,0.351,31,0
8,183,64,0,0,23.3,0.672,32,1
1,89,66,23,94,28.1,0.167,21,0
0,137,40,35,168,43.1,2.288,33,1
5,116,74,0,0,25.6,0.201,30,0
3,78,50,32,88,31.0,0.248,26,1
10,115,0,0,0,35.3,0.134,29,0
2,197,70,45,543,30.5,0.158,53,1
8,125,96,0,0,0.0,0.232,54,1
4,110,92,0,0,37.6,0.191,30,0
10,168,74,0,0,38.0,0.537,34,1
10,139,80,0,0,27.1,1.441,57,0
1,189,60,23,846,30.1,0.398,59,1
5,166,72,19,175,25.8,0.587,51,1
7,100,0,0,0,30.0,0.484,32,1
0,118,84,47,230,45.8,0.551,31,1
7,107,74,0,0,29.6,0.254,31,1
1,103,30,38,83,43.3,0.183,33,0
1,115,70,30,96,34.6,0.529,32,1
3,126,88,41,235,39.3,0.704,27,0
8,99,84,0,0,35.4,0.388,50,0
7,196,90,0,0,39.8,0.451,41,1
9,119,80,35,0,29.0,0.263,29,1
11,143,94,33,146,36.6,0.254,51,1
10,125,70,26,115,31.1,0.205,41,1
7,147,76,0,0,39.4,0.257,43,1
1,97,66,15,140,23.2,0.487,22,0
13,145,82,19,110,22.2,0.245,57,0
5,117,92,0,0,34.1,0.337,38,0`
  },
  {
    id: 'employees', name: 'Employee Attrition',
    tag: 'HR Analytics', rows: 30, cols: 9,
    desc: 'HR dataset — job roles, departments, missing salary, churn target',
    csv: `EmployeeID,Age,Department,JobRole,Gender,YearsAtCompany,MonthlyIncome,OverTime,Attrition
1001,41,Sales,Sales Executive,Female,6,5993,Yes,Yes
1002,49,Research,Research Scientist,Male,10,,No,No
1003,37,Research,Laboratory Technician,Male,0,2090,Yes,Yes
1004,33,Research,Research Scientist,Female,8,2909,Yes,No
1005,27,Research,Laboratory Technician,Male,2,3468,No,No
1006,32,Research,Laboratory Technician,Male,7,3068,No,No
1007,59,Research,Research Director,Female,1,2670,Yes,No
1008,30,Research,Laboratory Technician,Male,1,,No,No
1009,38,Research,Research Scientist,Male,9,9978,No,No
1010,36,Research,Laboratory Technician,Male,7,3298,No,No
1011,35,Research,Laboratory Technician,Male,5,2183,No,No
1012,29,Research,Research Scientist,Male,9,2500,No,No
1013,31,Sales,Sales Executive,Male,5,13500,Yes,No
1014,34,Research,Laboratory Technician,Male,8,2670,No,No
1015,28,Research,Laboratory Technician,Female,2,,Yes,Yes
1016,29,HR,Human Resources,Female,6,3498,No,No
1017,32,Research,Laboratory Technician,Male,10,3298,No,No
1018,22,Sales,Sales Representative,Male,0,2028,Yes,Yes
1019,53,Research,Research Scientist,Female,3,4364,No,No
1020,38,Sales,Sales Executive,Male,10,11592,No,No
1021,28,Research,Laboratory Technician,Male,3,2090,Yes,Yes
1022,45,Research,Research Director,Male,7,14940,No,No
1023,35,Research,Laboratory Technician,Female,15,4293,No,No
1024,29,Sales,Sales Representative,Male,2,1282,Yes,Yes
1025,31,Research,Laboratory Technician,Male,11,2670,No,No
1026,36,Research,Research Scientist,Male,6,5130,No,No
1027,29,Research,Laboratory Technician,Male,4,3458,No,No
1028,41,Research,Laboratory Technician,Male,5,,No,No
1029,34,Sales,Sales Executive,Male,8,9957,Yes,No
1030,30,Research,Laboratory Technician,Male,6,3298,No,No`
  },
  {
    id: 'wine', name: 'Wine Quality',
    tag: 'Regression', rows: 30, cols: 12,
    desc: 'Physicochemical wine properties — numeric features, outliers in acidity',
    csv: `fixed_acidity,volatile_acidity,citric_acid,residual_sugar,chlorides,free_sulfur_dioxide,total_sulfur_dioxide,density,pH,sulphates,alcohol,quality
7.4,0.70,0.00,1.9,0.076,11,34,0.9978,3.51,0.56,9.4,5
7.8,0.88,0.00,2.6,0.098,25,67,0.9968,3.20,0.68,9.8,5
7.8,0.76,0.04,2.3,0.092,15,54,0.9970,3.26,0.65,9.8,5
11.2,0.28,0.56,1.9,0.075,17,60,0.9980,3.16,0.58,9.8,6
7.4,0.70,0.00,1.9,0.076,11,34,0.9978,3.51,0.56,9.4,5
7.4,0.66,0.00,1.8,0.075,13,40,0.9978,3.51,0.56,9.4,5
7.9,0.60,0.06,1.6,0.069,15,59,0.9964,3.30,0.46,9.4,5
7.3,0.65,0.00,1.2,0.065,15,21,0.9946,3.39,0.47,10.0,7
7.8,0.58,0.02,2.0,0.073,9,18,0.9968,3.36,0.57,9.5,7
7.5,0.50,0.36,6.1,0.071,17,102,0.9978,3.35,0.80,10.5,5
6.7,0.58,0.08,1.8,0.097,15,65,0.9959,3.28,0.54,9.2,5
7.5,0.50,0.36,6.1,0.071,17,102,0.9978,3.35,0.80,10.5,5
5.6,0.615,0.00,1.6,0.089,16,59,0.9943,3.58,0.52,9.9,5
7.8,0.61,0.29,1.6,0.114,9,29,0.9974,3.26,1.56,9.1,5
8.9,0.62,0.18,3.8,0.176,52,145,0.9986,3.16,0.88,9.2,5
8.9,0.62,0.19,3.9,0.170,51,148,0.9986,3.17,0.93,9.2,5
8.5,0.28,0.56,1.8,0.092,35,103,0.9969,3.30,0.75,10.5,7
8.1,0.56,0.28,1.7,0.368,16,56,0.9968,3.11,1.28,9.3,5
7.4,0.59,0.08,4.4,0.086,6,29,0.9974,3.38,0.50,9.0,4
7.9,0.32,0.51,1.8,0.341,17,56,0.9969,3.04,1.08,9.2,6
8.9,0.22,0.48,1.8,0.077,29,60,0.9968,3.39,0.53,9.4,6
7.6,0.39,0.31,2.3,0.082,23,71,0.9982,3.52,0.65,9.7,5
7.9,0.43,0.21,1.6,0.106,10,37,0.9966,3.17,0.91,9.5,5
8.5,0.49,0.11,2.3,0.084,9,67,0.9968,3.17,0.53,9.4,5
6.9,0.40,0.14,2.4,0.085,21,40,0.9968,3.43,0.63,9.7,6
6.3,0.39,0.16,1.4,0.080,11,23,0.9955,3.34,0.56,9.3,5
7.6,0.41,0.24,1.8,0.080,4,11,0.9962,3.28,0.59,9.5,5
7.9,0.43,0.21,1.6,0.106,10,37,0.9966,3.17,0.91,9.5,5
,0.73,0.00,1.5,0.082,8,23,0.9949,3.41,0.55,9.4,5
7.2,0.23,0.32,8.5,0.058,47,186,0.9956,3.19,0.40,9.9,6`
  }
];

function loadSampleById(id) {
  const s = SAMPLES.find(x => x.id === id);
  if (!s) return;
  const file = new File([s.csv], `${s.name.replace(/\s+/g,'_').toLowerCase()}.csv`, {type:'text/csv'});
  doUpload(file);
}
