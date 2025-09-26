//Mock Data for John Doe (Customer ID: 3091 / Participant ID: 3091)
// UPDATED with Domain-Specific Recommendations

const JOHN_DOE_MOCK_DATA = {
  customer_info: {
    customer_id: 3091,
    participant_id: "3091",
    name: "John Doe",
    initials: "JD",
    email: "john.doe@example.com",
    age: 45,
    report_id: "MG3091",
    lab_name: "Lab_2 Diagnostics",
    upload_date: "2025-08-12",
    last_updated: "March 12, 2025"
  },

  // Your existing domain_bacteria stays exactly the same...
 domain_bacteria: {
    aging: {
      bacteria: [
        {
          msp_id: "msp_0137",
          bacteria_name: "Prevotella copri",
          full_name: "Prevotella copri",
          abundance: 0.0000018829,
          current_level: "1.9 units",
          percentage: 0.251,
          confidence_level: "C",
          status: "LOW",
          optimal_range: [0.000005, 0.00001],
          category: "beneficial",
          description: "Important for polysaccharide breakdown and anti-aging processes"
        },
        {
          msp_id: "msp_0987",
          bacteria_name: "Bacteroides thetaiotaomicron",
          full_name: "Bacteroides thetaiotaomicron",
          abundance: 0.0000014858,
          current_level: "1.5 units",
          percentage: 0.198,
          confidence_level: "C",
          status: "LOW",
          optimal_range: [0.000004, 0.000008],
          category: "beneficial",
          description: "Key player in carbohydrate metabolism and cellular aging"
        },
        {
          msp_id: "msp_1947",
          bacteria_name: "Lactobacillus longum",
          full_name: "Lactobacillus longum",
          abundance: 0.000000135,
          current_level: "0.1 units",
          percentage: 0.034,
          confidence_level: "C",
          status: "LOW",
          optimal_range: [0.000002, 0.000006],
          category: "probiotic",
          description: "Anti-aging probiotic, supports longevity pathways"
        },
        {
          msp_id: "msp_0866",
          bacteria_name: "Lactobacillus agilis",
          full_name: "Lactobacillus agilis",
          abundance: 0.0000004928,
          current_level: "0.5 units",
          percentage: 0.896,
          confidence_level: "C",
          status: "NORMAL",
          optimal_range: [0.0000003, 0.0000008],
          category: "probiotic",
          description: "Supports metabolic health and aging gracefully"
        },
        // NEW ADDITIONS FOR AGING DOMAIN
        {
          msp_id: "msp_aging_05",
          bacteria_name: "Akkermansia muciniphila",
          full_name: "Akkermansia muciniphila",
          abundance: 0.0000012456,
          current_level: "1.2 units",
          percentage: 0.312,
          confidence_level: "B",
          status: "LOW",
          optimal_range: [0.000003, 0.000008],
          category: "beneficial",
          description: "Mucin degrader, supports gut barrier and longevity"
        },
        {
          msp_id: "msp_aging_06",
          bacteria_name: "Bifidobacterium animalis",
          full_name: "Bifidobacterium animalis subsp. lactis",
          abundance: 0.0000008923,
          current_level: "0.9 units",
          percentage: 0.445,
          confidence_level: "C",
          status: "LOW",
          optimal_range: [0.000002, 0.000005],
          category: "probiotic",
          description: "Immune support and anti-inflammatory effects"
        },
        {
          msp_id: "msp_aging_07",
          bacteria_name: "Christensenella minuta",
          full_name: "Christensenella minuta",
          abundance: 0.0000003421,
          current_level: "0.3 units",
          percentage: 0.171,
          confidence_level: "C",
          status: "LOW",
          optimal_range: [0.000001, 0.000003],
          category: "beneficial",
          description: "Associated with longevity and healthy aging"
        },
        {
          msp_id: "msp_aging_08",
          bacteria_name: "Roseburia intestinalis",
          full_name: "Roseburia intestinalis",
          abundance: 0.0000005634,
          current_level: "0.6 units",
          percentage: 0.281,
          confidence_level: "C",
          status: "LOW",
          optimal_range: [0.000002, 0.000004],
          category: "beneficial",
          description: "Butyrate producer, anti-inflammatory"
        },
        {
          msp_id: "msp_aging_09",
          bacteria_name: "Eubacterium rectale",
          full_name: "Eubacterium rectale",
          abundance: 0.0000007821,
          current_level: "0.8 units",
          percentage: 0.391,
          confidence_level: "C",
          status: "LOW",
          optimal_range: [0.000002, 0.000005],
          category: "beneficial",
          description: "Major butyrate producer, supports healthy aging"
        },
        {
          msp_id: "msp_aging_10",
          bacteria_name: "Clostridium bolteae",
          full_name: "Clostridium bolteae",
          abundance: 0.0000015432,
          current_level: "1.5 units",
          percentage: 0.771,
          confidence_level: "C",
          status: "HIGH",
          optimal_range: [0.0000003, 0.0000008],
          category: "concerning",
          description: "May contribute to inflammation and accelerated aging"
        }
      ],
      scores: {
        diversity: 2.4,
        overall: 2.6,
        status: "poor"
      }
    },

    gut: {
      bacteria: [
        {
          msp_id: "msp_0421",
          bacteria_name: "Clostridium butyricum",
          full_name: "Clostridium butyricum",
          abundance: 0.0000006541,
          current_level: "0.7 units",
          percentage: 0.327,
          confidence_level: "C",
          status: "LOW",
          optimal_range: [0.000001, 0.000003],
          category: "beneficial",
          description: "Butyrate producer, essential for gut health"
        },
        {
          msp_id: "msp_1997",
          bacteria_name: "Ruminococcus bromii",
          full_name: "Ruminococcus bromii",
          abundance: 0.0000051789,
          current_level: "5.2 units",
          percentage: 0.863,
          confidence_level: "C",
          status: "NORMAL",
          optimal_range: [0.000004, 0.000008],
          category: "beneficial",
          description: "Key starch degrader in the gut microbiome"
        },
        {
          msp_id: "msp_0619",
          bacteria_name: "Faecalibacterium prausnitzii",
          full_name: "Faecalibacterium prausnitzii",
          abundance: 0.0000001106,
          current_level: "0.1 units",
          percentage: 0.031,
          confidence_level: "B",
          status: "LOW",
          optimal_range: [0.000002, 0.000005],
          category: "beneficial",
          description: "Anti-inflammatory bacteria, crucial for gut barrier function"
        },
        {
          msp_id: "msp_0921",
          bacteria_name: "Ruminococcus sp.",
          full_name: "Ruminococcus species UBA1828",
          abundance: 0.0000002678,
          current_level: "0.3 units",
          percentage: 0.357,
          confidence_level: "C",
          status: "LOW",
          optimal_range: [0.0000005, 0.000001],
          category: "beneficial",
          description: "Fiber fermenter, supports digestive health"
        },
        // NEW ADDITIONS FOR GUT DOMAIN
        {
          msp_id: "msp_gut_05",
          bacteria_name: "Bacteroides fragilis",
          full_name: "Bacteroides fragilis",
          abundance: 0.0000034567,
          current_level: "3.5 units",
          percentage: 1.728,
          confidence_level: "B",
          status: "NORMAL",
          optimal_range: [0.000003, 0.000006],
          category: "beneficial",
          description: "Important for immune system development and gut health"
        },
        {
          msp_id: "msp_gut_06",
          bacteria_name: "Bacteroides uniformis",
          full_name: "Bacteroides uniformis",
          abundance: 0.0000028934,
          current_level: "2.9 units",
          percentage: 1.447,
          confidence_level: "C",
          status: "NORMAL",
          optimal_range: [0.000002, 0.000005],
          category: "beneficial",
          description: "Polysaccharide degrader, supports metabolic health"
        },
        {
          msp_id: "msp_gut_07",
          bacteria_name: "Blautia obeum",
          full_name: "Blautia obeum",
          abundance: 0.0000012345,
          current_level: "1.2 units",
          percentage: 0.617,
          confidence_level: "C",
          status: "LOW",
          optimal_range: [0.000002, 0.000004],
          category: "beneficial",
          description: "Butyrate producer, supports intestinal health"
        },
        {
          msp_id: "msp_gut_08",
          bacteria_name: "Coprococcus eutactus",
          full_name: "Coprococcus eutactus",
          abundance: 0.0000008765,
          current_level: "0.9 units",
          percentage: 0.438,
          confidence_level: "C",
          status: "LOW",
          optimal_range: [0.000002, 0.000004],
          category: "beneficial",
          description: "Butyrate producer, anti-inflammatory properties"
        },
        {
          msp_id: "msp_gut_09",
          bacteria_name: "Bacteroides ovatus",
          full_name: "Bacteroides ovatus",
          abundance: 0.0000023456,
          current_level: "2.3 units",
          percentage: 1.173,
          confidence_level: "C",
          status: "NORMAL",
          optimal_range: [0.000002, 0.000005],
          category: "beneficial",
          description: "Complex carbohydrate degrader"
        },
        {
          msp_id: "msp_gut_10",
          bacteria_name: "Parabacteroides distasonis",
          full_name: "Parabacteroides distasonis",
          abundance: 0.0000015432,
          current_level: "1.5 units",
          percentage: 0.772,
          confidence_level: "C",
          status: "NORMAL",
          optimal_range: [0.000001, 0.000003],
          category: "beneficial",
          description: "Supports gut barrier function and immune modulation"
        },
        {
          msp_id: "msp_gut_11",
          bacteria_name: "Escherichia coli",
          full_name: "Escherichia coli",
          abundance: 0.0000032145,
          current_level: "3.2 units",
          percentage: 1.607,
          confidence_level: "B",
          status: "HIGH",
          optimal_range: [0.0000005, 0.000002],
          category: "concerning",
          description: "Can be pathogenic when overgrown, causes inflammation"
        },
        {
          msp_id: "msp_gut_12",
          bacteria_name: "Alistipes putredinis",
          full_name: "Alistipes putredinis",
          abundance: 0.0000019876,
          current_level: "2.0 units",
          percentage: 0.994,
          confidence_level: "C",
          status: "NORMAL",
          optimal_range: [0.000001, 0.000003],
          category: "neutral",
          description: "Common gut bacteria with neutral impact"
        }
      ],
      scores: {
        diversity: 3.0,
        overall: 3.2,
        status: "good"
      }
    },

    liver: {
      bacteria: [
        {
          msp_id: "msp_0704",
          bacteria_name: "Enterococcus faecium",
          full_name: "Enterococcus faecium",
          abundance: 0.0000003832,
          current_level: "2.6 units",
          percentage: 2.555,
          confidence_level: "C",
          status: "HIGH",
          optimal_range: [0.0000001, 0.0000002],
          category: "concerning",
          description: "Potential pathogen, elevated levels may stress liver function"
        },
        {
          msp_id: "msp_0939",
          bacteria_name: "Lactobacillus rhamnosus",
          full_name: "Lactobacillus rhamnosus",
          abundance: 0.0000000431,
          current_level: "0.04 units",
          percentage: 0.022,
          confidence_level: "C",
          status: "LOW",
          optimal_range: [0.000001, 0.000003],
          category: "probiotic",
          description: "Liver-protective probiotic, supports detoxification"
        },
        {
          msp_id: "msp_2050",
          bacteria_name: "Clostridium perfringens",
          full_name: "Clostridium perfringens Family XIII",
          abundance: 0.000000148,
          current_level: "1.9 units",
          percentage: 1.973,
          confidence_level: "C",
          status: "HIGH",
          optimal_range: [0.00000005, 0.0000001],
          category: "pathogen",
          description: "Toxin producer, can burden liver detoxification systems"
        },
        {
          msp_id: "msp_1725",
          bacteria_name: "Blautia sp.",
          full_name: "Blautia species",
          abundance: 0.0000000426,
          current_level: "0.2 units",
          percentage: 0.213,
          confidence_level: "C",
          status: "LOW",
          optimal_range: [0.0000001, 0.0000003],
          category: "beneficial",
          description: "Supports liver metabolism and bile acid processing"
        },
        // NEW ADDITIONS FOR LIVER DOMAIN
        {
          msp_id: "msp_liver_05",
          bacteria_name: "Lactobacillus casei",
          full_name: "Lactobacillus casei",
          abundance: 0.0000000832,
          current_level: "0.08 units",
          percentage: 0.042,
          confidence_level: "C",
          status: "LOW",
          optimal_range: [0.000001, 0.000003],
          category: "probiotic",
          description: "Supports liver health and detoxification pathways"
        },
        {
          msp_id: "msp_liver_06",
          bacteria_name: "Bifidobacterium breve",
          full_name: "Bifidobacterium breve",
          abundance: 0.0000001234,
          current_level: "0.12 units",
          percentage: 0.062,
          confidence_level: "C",
          status: "LOW",
          optimal_range: [0.000001, 0.000004],
          category: "probiotic",
          description: "Anti-inflammatory, supports liver function"
        },
        {
          msp_id: "msp_liver_07",
          bacteria_name: "Klebsiella pneumoniae",
          full_name: "Klebsiella pneumoniae",
          abundance: 0.0000002145,
          current_level: "1.8 units",
          percentage: 1.823,
          confidence_level: "B",
          status: "HIGH",
          optimal_range: [0.00000005, 0.0000001],
          category: "pathogen",
          description: "Opportunistic pathogen, produces toxins affecting liver"
        },
        {
          msp_id: "msp_liver_08",
          bacteria_name: "Enterococcus faecalis",
          full_name: "Enterococcus faecalis",
          abundance: 0.0000001876,
          current_level: "1.5 units",
          percentage: 1.502,
          confidence_level: "C",
          status: "HIGH",
          optimal_range: [0.00000005, 0.0000001],
          category: "concerning",
          description: "Can produce ammonia, burdening liver detox"
        },
        {
          msp_id: "msp_liver_09",
          bacteria_name: "Streptococcus mutans",
          full_name: "Streptococcus mutans",
          abundance: 0.0000001432,
          current_level: "1.2 units",
          percentage: 1.234,
          confidence_level: "C",
          status: "HIGH",
          optimal_range: [0.00000002, 0.00000008],
          category: "concerning",
          description: "Associated with systemic inflammation affecting liver"
        },
        {
          msp_id: "msp_liver_10",
          bacteria_name: "Clostridium difficile",
          full_name: "Clostridium difficile",
          abundance: 0.0000000987,
          current_level: "0.98 units",
          percentage: 0.987,
          confidence_level: "B",
          status: "HIGH",
          optimal_range: [0.00000001, 0.00000005],
          category: "pathogen",
          description: "Toxin producer, major liver stressor"
        },
        {
          msp_id: "msp_liver_11",
          bacteria_name: "Bacteroides vulgatus",
          full_name: "Bacteroides vulgatus",
          abundance: 0.0000000654,
          current_level: "0.65 units",
          percentage: 0.327,
          confidence_level: "C",
          status: "LOW",
          optimal_range: [0.000001, 0.000003],
          category: "beneficial",
          description: "Supports bile acid metabolism"
        },
        {
          msp_id: "msp_liver_12",
          bacteria_name: "Prevotella melaninogenica",
          full_name: "Prevotella melaninogenica",
          abundance: 0.0000000543,
          current_level: "0.54 units",
          percentage: 0.272,
          confidence_level: "C",
          status: "LOW",
          optimal_range: [0.000001, 0.000002],
          category: "neutral",
          description: "Limited impact on liver function"
        }
      ],
      scores: {
        diversity: 2.5,
        overall: 2.8,
        status: "poor"
      }
    },

    heart: {
      bacteria: [
        {
          msp_id: "msp_0736",
          bacteria_name: "Bacteroides fragilis",
          full_name: "Bacteroides fragilis An322",
          abundance: 0.0000027543,
          current_level: "2.8 units",
          percentage: 0.918,
          evidence_strength: "C",
          status: "NORMAL",
          optimal_range: [0.000002, 0.000004],
          category: "beneficial",
          description: "Supports cardiovascular health through immune modulation"
        },
        {
          msp_id: "msp_0357",
          bacteria_name: "Clostridium sp.",
          full_name: "Clostridium species CAG-81",
          abundance: 0.0000010672,
          current_level: "0.7 units",
          percentage: 0.711,
          evidence_strength: "C",
          status: "NORMAL",
          optimal_range: [0.000001, 0.000002],
          category: "neutral",
          description: "Neutral impact on cardiovascular system"
        },
        // NEW ADDITIONS FOR HEART DOMAIN
        {
          msp_id: "msp_heart_03",
          bacteria_name: "Roseburia hominis",
          full_name: "Roseburia hominis",
          abundance: 0.0000023456,
          current_level: "2.3 units",
          percentage: 1.173,
          confidence_level: "B",
          status: "NORMAL",
          optimal_range: [0.000002, 0.000005],
          category: "beneficial",
          description: "Butyrate producer, reduces cardiovascular inflammation"
        },
        {
          msp_id: "msp_heart_04",
          bacteria_name: "Lactobacillus plantarum",
          full_name: "Lactobacillus plantarum",
          abundance: 0.0000018765,
          current_level: "1.9 units",
          percentage: 0.938,
          confidence_level: "B",
          status: "NORMAL",
          optimal_range: [0.000001, 0.000004],
          category: "probiotic",
          description: "Cardioprotective probiotic, lowers cholesterol"
        },
        {
          msp_id: "msp_heart_05",
          bacteria_name: "Bifidobacterium lactis",
          full_name: "Bifidobacterium animalis subsp. lactis",
          abundance: 0.0000015432,
          current_level: "1.5 units",
          percentage: 0.772,
          confidence_level: "C",
          status: "NORMAL",
          optimal_range: [0.000001, 0.000003],
          category: "probiotic",
          description: "Supports heart health through lipid metabolism"
        },
        {
          msp_id: "msp_heart_06",
          bacteria_name: "Eubacterium eligens",
          full_name: "Eubacterium eligens",
          abundance: 0.0000012345,
          current_level: "1.2 units",
          percentage: 0.617,
          confidence_level: "C",
          status: "LOW",
          optimal_range: [0.000002, 0.000004],
          category: "beneficial",
          description: "Produces short-chain fatty acids benefiting heart health"
        },
        {
          msp_id: "msp_heart_07",
          bacteria_name: "Streptococcus thermophilus",
          full_name: "Streptococcus thermophilus",
          abundance: 0.0000009876,
          current_level: "1.0 units",
          percentage: 0.494,
          confidence_level: "C",
          status: "NORMAL",
          optimal_range: [0.0000008, 0.000002],
          category: "probiotic",
          description: "Fermentative bacteria with cardiovascular benefits"
        },
        {
          msp_id: "msp_heart_08",
          bacteria_name: "Enterococcus hirae",
          full_name: "Enterococcus hirae",
          abundance: 0.0000021098,
          current_level: "2.1 units",
          percentage: 1.055,
          confidence_level: "C",
          status: "HIGH",
          optimal_range: [0.0000005, 0.000001],
          category: "concerning",
          description: "May contribute to cardiovascular inflammation"
        },
        {
          msp_id: "msp_heart_09",
          bacteria_name: "Parabacteroides goldsteinii",
          full_name: "Parabacteroides goldsteinii",
          abundance: 0.0000008765,
          current_level: "0.9 units",
          percentage: 0.438,
          confidence_level: "C",
          status: "NORMAL",
          optimal_range: [0.0000005, 0.000002],
          category: "neutral",
          description: "Neutral cardiovascular impact"
        }
      ],
      scores: {
        diversity: 3.1,
        overall: 3.5,
        status: "good"
      }
    },

    skin: {
      bacteria: [
        {
          msp_id: "msp_skin_01",
          bacteria_name: "Staphylococcus epidermidis",
          full_name: "Staphylococcus epidermidis",
          abundance: 0.000002156,
          current_level: "2.2 units",
          percentage: 1.078,
          confidence_level: "B",
          status: "NORMAL",
          optimal_range: [0.000001, 0.000003],
          category: "beneficial",
          description: "Protective skin commensal, maintains barrier function"
        },
        {
          msp_id: "msp_skin_02",
          bacteria_name: "Cutibacterium acnes",
          full_name: "Cutibacterium acnes",
          abundance: 0.000001897,
          current_level: "2.5 units",
          percentage: 2.533,
          evidence_strength: "C",
          status: "HIGH",
          optimal_range: [0.0000005, 0.000001],
          category: "concerning",
          description: "Can cause skin inflammation when overgrown"
        },
        // NEW ADDITIONS FOR SKIN DOMAIN
        {
          msp_id: "msp_skin_03",
          bacteria_name: "Lactobacillus acidophilus",
          full_name: "Lactobacillus acidophilus",
          abundance: 0.0000008765,
          current_level: "0.9 units",
          percentage: 0.438,
          confidence_level: "C",
          status: "LOW",
          optimal_range: [0.000002, 0.000005],
          category: "probiotic",
          description: "Supports skin health and reduces inflammation"
        },
        {
          msp_id: "msp_skin_04",
          bacteria_name: "Corynebacterium kroppenstedtii",
          full_name: "Corynebacterium kroppenstedtii",
          abundance: 0.0000012345,
          current_level: "1.2 units",
          percentage: 0.617,
          confidence_level: "C",
          status: "NORMAL",
          optimal_range: [0.000001, 0.000002],
          category: "beneficial",
          description: "Normal skin commensal, protective function"
        },
        {
          msp_id: "msp_skin_05",
          bacteria_name: "Staphylococcus hominis",
          full_name: "Staphylococcus hominis",
          abundance: 0.0000015432,
          current_level: "1.5 units",
          percentage: 0.772,
          confidence_level: "C",
          status: "NORMAL",
          optimal_range: [0.000001, 0.000003],
          category: "beneficial",
          description: "Beneficial skin bacteria, antimicrobial properties"
        },
        {
          msp_id: "msp_skin_06",
          bacteria_name: "Malassezia restricta",
          full_name: "Malassezia restricta",
          abundance: 0.0000018765,
          current_level: "1.9 units",
          percentage: 0.938,
          confidence_level: "C",
          status: "HIGH",
          optimal_range: [0.0000003, 0.0000008],
          category: "concerning",
          description: "Can cause skin irritation and seborrheic dermatitis"
        },
        {
          msp_id: "msp_skin_07",
          bacteria_name: "Streptococcus pyogenes",
          full_name: "Streptococcus pyogenes",
          abundance: 0.0000009876,
          current_level: "1.0 units",
          percentage: 0.494,
          confidence_level: "B",
          status: "HIGH",
          optimal_range: [0.00000001, 0.00000005],
          category: "pathogen",
          description: "Pathogenic, can cause serious skin infections"
        },
        {
          msp_id: "msp_skin_08",
          bacteria_name: "Micrococcus luteus",
          full_name: "Micrococcus luteus",
          abundance: 0.0000007654,
          current_level: "0.8 units",
          percentage: 0.383,
          confidence_level: "C",
          status: "NORMAL",
          optimal_range: [0.0000005, 0.000002],
          category: "beneficial",
          description: "Protective skin bacteria with antimicrobial activity"
        },
        {
          msp_id: "msp_skin_09",
          bacteria_name: "Prevotella melaninogenica",
          full_name: "Prevotella melaninogenica",
          abundance: 0.0000005432,
          current_level: "0.5 units",
          percentage: 0.272,
          confidence_level: "C",
          status: "LOW",
          optimal_range: [0.000001, 0.000002],
          category: "neutral",
          description: "Limited skin impact, normal commensal"
        }
      ],
      scores: {
        diversity: 2.9,
        overall: 2.7,
        status: "warning"
      }
    },

    cognitive: {
      bacteria: [
        {
          msp_id: "msp_brain_01",
          bacteria_name: "Lactobacillus helveticus",
          full_name: "Lactobacillus helveticus",
          abundance: 0.000001234,
          current_level: "0.4 units",
          percentage: 0.353,
          confidence_level: "A",
          status: "LOW",
          optimal_range: [0.000002, 0.000005],
          category: "probiotic",
          description: "Psychobiotic strain, supports cognitive function and mood"
        },
        {
          msp_id: "msp_brain_02",
          bacteria_name: "Bifidobacterium longum",
          full_name: "Bifidobacterium longum",
          abundance: 0.000003456,
          current_level: "3.5 units",
          percentage: 0.768,
          confidence_level: "A",
          status: "NORMAL",
          optimal_range: [0.000003, 0.000006],
          category: "probiotic",
          description: "Gut-brain axis modulator, enhances memory and learning"
        },
        // NEW ADDITIONS FOR COGNITIVE DOMAIN
        {
          msp_id: "msp_brain_03",
          bacteria_name: "Lactobacillus reuteri",
          full_name: "Lactobacillus reuteri",
          abundance: 0.0000018765,
          current_level: "1.9 units",
          percentage: 0.938,
          confidence_level: "B",
          status: "NORMAL",
          optimal_range: [0.000001, 0.000004],
          category: "probiotic",
          description: "Produces GABA, supports mood and cognitive function"
        },
        {
          msp_id: "msp_brain_04",
          bacteria_name: "Bifidobacterium breve",
          full_name: "Bifidobacterium breve",
          abundance: 0.0000012345,
          current_level: "1.2 units",
          percentage: 0.617,
          confidence_level: "B",
          status: "LOW",
          optimal_range: [0.000002, 0.000005],
          category: "probiotic",
          description: "Neuroprotective effects, reduces anxiety and depression"
        },
        {
          msp_id: "msp_brain_05",
          bacteria_name: "Enterococcus faecium",
          full_name: "Enterococcus faecium",
          abundance: 0.0000021098,
          current_level: "2.1 units",
          percentage: 1.055,
          confidence_level: "C",
          status: "HIGH",
          optimal_range: [0.0000003, 0.0000008],
          category: "concerning",
          description: "May contribute to neuroinflammation and cognitive decline"
        },
        {
          msp_id: "msp_brain_06",
          bacteria_name: "Lactobacillus casei",
          full_name: "Lactobacillus casei",
          abundance: 0.0000009876,
          current_level: "1.0 units",
          percentage: 0.494,
          confidence_level: "C",
          status: "LOW",
          optimal_range: [0.000002, 0.000004],
          category: "probiotic",
          description: "Supports neurotransmitter production, enhances mood"
        },
        {
          msp_id: "msp_brain_07",
          bacteria_name: "Streptococcus thermophilus",
          full_name: "Streptococcus thermophilus",
          abundance: 0.0000015432,
          current_level: "1.5 units",
          percentage: 0.772,
          confidence_level: "C",
          status: "NORMAL",
          optimal_range: [0.000001, 0.000003],
          category: "probiotic",
          description: "Produces folate, supports cognitive health"
        },
        {
          msp_id: "msp_brain_08",
          bacteria_name: "Clostridium butyricum",
          full_name: "Clostridium butyricum",
          abundance: 0.0000008765,
          current_level: "0.9 units",
          percentage: 0.438,
          confidence_level: "C",
          status: "LOW",
          optimal_range: [0.000002, 0.000004],
          category: "beneficial",
          description: "Butyrate producer, supports brain health via gut-brain axis"
        },
        {
          msp_id: "msp_brain_09",
          bacteria_name: "Akkermansia muciniphila",
          full_name: "Akkermansia muciniphila",
          abundance: 0.0000007654,
          current_level: "0.8 units",
          percentage: 0.383,
          confidence_level: "B",
          status: "LOW",
          optimal_range: [0.000002, 0.000006],
          category: "beneficial",
          description: "Supports gut barrier, indirectly benefits cognitive function"
        },
        {
          msp_id: "msp_brain_10",
          bacteria_name: "Prevotella copri",
          full_name: "Prevotella copri",
          abundance: 0.0000005432,
          current_level: "0.5 units",
          percentage: 0.272,
          confidence_level: "C",
          status: "LOW",
          optimal_range: [0.000001, 0.000003],
          category: "neutral",
          description: "Limited direct cognitive impact"
        },
        {
          msp_id: "msp_brain_11",
          bacteria_name: "Bacteroides thetaiotaomicron",
          full_name: "Bacteroides thetaiotaomicron",
          abundance: 0.0000006789,
          current_level: "0.7 units",
          percentage: 0.339,
          confidence_level: "C",
          status: "LOW",
          optimal_range: [0.000001, 0.000003],
          category: "beneficial",
          description: "Supports overall gut health, indirect cognitive benefits"
        },
        {
          msp_id: "msp_brain_12",
          bacteria_name: "Escherichia coli",
          full_name: "Escherichia coli",
          abundance: 0.0000013579,
          current_level: "1.4 units",
          percentage: 0.679,
          confidence_level: "B",
          status: "HIGH",
          optimal_range: [0.0000002, 0.0000006],
          category: "concerning",
          description: "Can produce toxins affecting brain function via gut-brain axis"
        }],
      scores: {
        diversity: 2.9,
        overall: 2.7,
        status: "warning"
      }
    }
  },

  // Your existing overall_health and clinical_notes stay the same...
  overall_health: {
    diversity_score: 2.8,
    overall_score: 3.0,
    status: "warning",
    total_bacteria_analyzed: 16,
    concerning_bacteria: 4,
    beneficial_bacteria: 10,
    neutral_bacteria: 2
  },

  clinical_notes: {
    primary_concerns: [
      "Low beneficial bacteria in aging and liver domains",
      "Elevated pathogenic bacteria affecting liver function",
      "Suboptimal gut-brain axis function"
    ],
    recommendations: [
      "Increase probiotic intake focusing on Lactobacillus strains",
      "Reduce processed foods to lower pathogenic bacteria",
      "Consider liver support supplements",
      "Focus on prebiotic fiber intake"
    ]
  },

  // ✅ REPLACE YOUR OLD RECOMMENDATIONS SECTION WITH THIS NEW ONE:
  recommendations: {
    // ===== GENERAL RECOMMENDATIONS (applies to all domains) =====
    probiotics: [
      {
        id: 'high_potency_multi_strain',
        title: 'High-Potency Multi-Strain Probiotic',
        description: 'Comprehensive probiotic to restore severely depleted beneficial bacteria',
        dosage: '50-100 billion CFU daily',
        duration: '6 months',
        reason: 'Multiple low beneficial bacteria across domains',
        evidence_level: 'strong',
        priority: 1,
        is_recommended: true,
        key_strains: [
          'Lactobacillus rhamnosus (liver support)',
          'Faecalibacterium prausnitzii (gut barrier)',
          'Lactobacillus longum (aging support)',
          'Bifidobacterium animalis (immune support)',
          'Akkermansia muciniphila (metabolic health)'
        ]
      },
      {
        id: 'lactobacillus_rhamnosus',
        title: 'Lactobacillus rhamnosus (Liver-Specific)',
        description: 'Targeted strain for liver detoxification support',
        dosage: '20 billion CFU daily',
        duration: '6 months',
        reason: 'Extremely low levels (0.04 units) affecting liver function',
        evidence_level: 'strong',
        priority: 1,
        is_recommended: true,
        benefits: [
          'Supports liver detoxification pathways',
          'Reduces inflammatory burden on liver',
          'Helps metabolize toxins',
          'Protects against fatty liver'
        ]
      },
      {
        id: 'faecalibacterium_prausnitzii',
        title: 'Faecalibacterium prausnitzii',
        description: 'Critical anti-inflammatory gut bacteria',
        dosage: '10 billion CFU daily',
        duration: '6 months',
        reason: 'Critically low levels (0.1 units) compromising gut barrier',
        evidence_level: 'strong',
        priority: 1,
        is_recommended: true,
        benefits: [
          'Strengthens intestinal barrier',
          'Produces anti-inflammatory compounds',
          'Reduces systemic inflammation',
          'Supports immune regulation'
        ]
      }
    ],

    supplements: [
      {
        id: 'milk_thistle_liver',
        title: 'Milk Thistle (Silymarin)',
        description: 'Premier liver regeneration and protection',
        dosage: '400mg twice daily',
        duration: '6 months',
        reason: 'Combat toxin damage from pathogenic bacteria (Enterococcus, Clostridium)',
        evidence_level: 'strong',
        priority: 1,
        is_recommended: true,
        benefits: [
          'Regenerates liver cells',
          'Protects from toxins',
          'Reduces liver enzymes',
          'Supports bile production'
        ]
      },
      {
        id: 'l_glutamine_gut',
        title: 'L-Glutamine',
        description: 'Primary fuel for intestinal cells and liver support',
        dosage: '15g daily (5g, 3x daily)',
        duration: '4 months',
        reason: 'Repair gut lining and reduce bacterial translocation to liver',
        evidence_level: 'strong',
        priority: 1,
        is_recommended: true,
        benefits: [
          'Heals leaky gut syndrome',
          'Fuels intestinal cell repair',
          'Reduces gut inflammation',
          'Supports liver detoxification'
        ]
      },
      {
        id: 'resveratrol_aging',
        title: 'Trans-Resveratrol',
        description: 'Powerful longevity compound and sirtuin activator',
        dosage: '500mg daily with meals',
        duration: 'Ongoing',
        reason: 'Activate longevity genes due to poor aging scores (2.6)',
        evidence_level: 'strong',
        priority: 1,
        is_recommended: true,
        benefits: [
          'Activates SIRT1 longevity genes',
          'Reduces inflammation',
          'Protects against oxidative stress',
          'Supports healthy aging'
        ]
      },
      {
        id: 'omega3_complex',
        title: 'High-Quality Omega-3 Complex',
        description: 'Anti-inflammatory support for multiple domains',
        dosage: '2g daily (1g EPA, 1g DHA)',
        duration: 'Ongoing',
        reason: 'Systemic inflammation from bacterial imbalances',
        evidence_level: 'strong',
        priority: 2,
        is_recommended: true,
        benefits: [
          'Reduces systemic inflammation',
          'Supports liver function',
          'Improves gut barrier integrity',
          'Protects against aging'
        ]
      },
      {
        id: 'nac_liver',
        title: 'N-Acetyl Cysteine (NAC)',
        description: 'Master antioxidant for liver detox',
        dosage: '600mg twice daily',
        duration: '4 months',
        reason: 'Boost glutathione for detoxification support',
        evidence_level: 'strong',
        priority: 2,
        is_recommended: true,
        benefits: [
          'Boosts glutathione production',
          'Protects liver from oxidative damage',
          'Supports cellular detoxification',
          'Reduces inflammation'
        ]
      }
    ],

    diet: [
      {
        id: 'liver_detox_foods',
        title: 'Liver Detoxification Diet',
        description: 'Foods that support liver detox pathways',
        dosage: 'Daily incorporation',
        duration: 'Ongoing',
        reason: 'Support Phase I & II detoxification enzymes due to pathogenic burden',
        evidence_level: 'strong',
        priority: 1,
        is_recommended: true,
        specific_foods: [
          'Cruciferous vegetables (broccoli, kale, cabbage)',
          'Sulfur-rich foods (garlic, onions)',
          'Beets and carrots',
          'Dandelion greens',
          'Artichokes',
          'Green tea (liver protective)',
          'Turmeric with black pepper'
        ]
      },
      {
        id: 'gut_healing_diet',
        title: 'Gut Restoration Protocol',
        description: 'Anti-inflammatory, gut-healing foods',
        dosage: 'Strict adherence',
        duration: '3 months',
        reason: 'Heal gut lining and restore beneficial bacteria (low F. prausnitzii)',
        evidence_level: 'strong',
        priority: 1,
        is_recommended: true,
        specific_foods: [
          'Bone broth (daily)',
          'Fermented vegetables (sauerkraut, kimchi)',
          'Kefir and yogurt with live cultures',
          'Prebiotic-rich foods (garlic, onions, leeks)',
          'Cooked vegetables (easier to digest)',
          'Wild-caught fish',
          'Organic, grass-fed meats'
        ]
      },
      {
        id: 'longevity_foods',
        title: 'Anti-Aging Superfoods',
        description: 'Mediterranean-style eating with longevity compounds',
        dosage: 'Daily incorporation',
        duration: 'Ongoing',
        reason: 'Support anti-aging pathways and reduce inflammation (aging score 2.6)',
        evidence_level: 'strong',
        priority: 1,
        is_recommended: true,
        specific_foods: [
          'Wild blueberries (1 cup daily)',
          'Extra virgin olive oil (3 tbsp daily)',
          'Walnuts and almonds (1 oz daily)',
          'Green tea (3 cups daily)',
          'Dark chocolate 85%+ (1 oz daily)',
          'Pomegranate juice (4 oz daily)'
        ]
      },
      {
        id: 'eliminate_toxins',
        title: 'Eliminate Toxic Foods',
        description: 'Remove foods that burden liver and damage gut',
        dosage: 'Complete elimination',
        duration: '6 months minimum',
        reason: 'Reduce liver workload and gut inflammation',
        evidence_level: 'strong',
        priority: 1,
        is_recommended: true,
        avoid_foods: [
          'Alcohol (complete elimination)',
          'Processed foods and additives',
          'High fructose corn syrup',
          'Trans fats and fried foods',
          'Gluten-containing grains',
          'Artificial sweeteners'
        ]
      }
    ],

    lifestyle: [
      {
        id: 'stress_gut_management',
        title: 'Gut-Brain Stress Protocol',
        description: 'Manage stress to support gut healing and liver function',
        dosage: 'Daily practice',
        duration: 'Ongoing',
        reason: 'Stress directly damages gut lining and increases liver burden',
        evidence_level: 'strong',
        priority: 1,
        is_recommended: true,
        techniques: [
          'Diaphragmatic breathing (10 min, 3x daily)',
          'Meditation or mindfulness practice',
          'Gentle yoga or tai chi',
          'Nature walks',
          'Adequate sleep (7-9 hours)'
        ]
      },
      {
        id: 'liver_support_routine',
        title: 'Daily Liver Support Routine',
        description: 'Morning liver flush and evening support',
        dosage: 'Daily practice',
        duration: 'Ongoing',
        reason: 'Optimize liver function and detoxification',
        evidence_level: 'moderate',
        priority: 2,
        is_recommended: true,
        routine: [
          'Warm lemon water upon waking',
          'Dry brushing before shower',
          'Castor oil pack 2x/week',
          'Early dinner (6 PM) for liver rest'
        ]
      },
      {
        id: 'longevity_exercise',
        title: 'Anti-Aging Exercise Protocol',
        description: 'Resistance training and cardio for longevity',
        dosage: '5x per week (3x strength, 2x cardio)',
        duration: 'Ongoing',
        reason: 'Combat age-related decline and improve bacterial diversity',
        evidence_level: 'strong',
        priority: 1,
        is_recommended: true,
        activities: [
          'Strength training (3x/week, 45 min)',
          'HIIT cardio (2x/week, 20 min)',
          'Daily walks (30 min)',
          'Flexibility work (yoga, stretching)'
        ]
      },
      {
        id: 'sleep_optimization_comprehensive',
        title: 'Comprehensive Sleep Protocol',
        description: 'Optimize sleep for gut healing, liver detox, and longevity',
        dosage: '7-9 hours nightly',
        duration: 'Ongoing',
        reason: 'Sleep is critical for gut repair, liver detox, and anti-aging',
        evidence_level: 'strong',
        priority: 1,
        is_recommended: true,
        protocol: [
          'Consistent sleep schedule (same time daily)',
          'Dark, cool room (65-68°F)',
          'No screens 2 hours before bed',
          'Magnesium glycinate before bed',
          'Blackout curtains and eye mask'
        ]
      }
    ],

    // ===== DOMAIN-SPECIFIC ADDITIONAL RECOMMENDATIONS =====
    domain_specific: {
      aging: {
        supplements: ['NAD+ precursor (250mg daily)', 'Spermidine (10mg daily)'],

        lifestyle: ['Intermittent fasting (16:8)', 'Cold therapy (3x/week)'],
        diet: [
      'Mediterranean diet with high polyphenol foods (berries, dark chocolate, green tea)',
      'Intermittent fasting 16:8 protocol to activate autophagy',
      'Include longevity foods: walnuts, olive oil, fatty fish 3x/week',
      'Limit processed foods and refined sugars to reduce AGEs formation',
      'Add resveratrol-rich foods: red grapes, dark berries, red wine (moderate)'
    ]
      },
      liver: {
        supplements: ['Alpha Lipoic Acid (300mg daily)', 'Selenium (200mcg daily)'],
        lifestyle: ['Eliminate all alcohol', 'Regular sauna sessions'],
        diet: [
      'Cruciferous vegetables daily: broccoli, kale, Brussels sprouts, cauliflower',
      'Sulfur-rich foods: garlic, onions, eggs, cruciferous vegetables',
      'Eliminate alcohol completely for 3 months minimum',
      'Include milk thistle tea and dandelion greens',
      'Add beets and carrots for liver detox support',
      'Reduce processed foods by 90% to minimize liver burden'
    ]
      },
      skin: {
        supplements: ['Zinc bisglycinate (30mg daily)', 'Vitamin D3 (2000 IU daily)'],
        diet: [
      'Eliminate dairy products for 4 weeks to reduce inflammation',
      'Low glycemic index foods to prevent insulin spikes',
      'Collagen-supporting foods: bone broth, vitamin C rich fruits, zinc-rich foods',
      'Anti-inflammatory omega-3 rich foods: wild salmon, sardines, walnuts',
      'Hydrating foods: cucumber, watermelon, leafy greens'
    ]
      },
      cognitive: {
        supplements: ['Lions Mane mushroom (1000mg daily)', 'Phosphatidylserine (300mg daily)'],
        lifestyle: ['Daily brain training', 'Learn new skills'],
        diet: [
      'Brain-healthy fats: avocados, nuts, seeds, fatty fish',
      'Blueberries and dark berries for cognitive protection',
      'Turmeric with black pepper for neuroinflammation',
      'Dark leafy greens for folate and brain health',
      'Limit refined carbs that cause blood sugar spikes'
    ]
      },
      gut: {
        supplements: ['Butyrate supplement (1200mg daily)', 'Digestive enzymes with meals'],
        diet: ['Eliminate gluten completely', 'Focus on prebiotic fibers']
      },
      heart: {
        supplements: ['CoQ10 (200mg daily)', 'Magnesium glycinate (400mg daily)'],
        lifestyle: ['Mediterranean diet adherence', 'Regular cardio exercise'],
        diet: [
      'Mediterranean diet pattern with emphasis on olive oil',
      'Fatty fish 2-3 times per week for omega-3s',
      'Nuts and seeds daily (especially walnuts and flaxseeds)',
      'Limit sodium intake to under 2000mg daily',
      'Include potassium-rich foods: bananas, sweet potatoes, spinach'
    ]
      }
    }
  }
};

export default JOHN_DOE_MOCK_DATA;

