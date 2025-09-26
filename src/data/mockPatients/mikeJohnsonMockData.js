// Mock Data for Mike Johnson (Customer ID: 5500 / Participant ID: 5500)
// Patient-friendly current_level values instead of scientific notation

const MIKE_JOHNSON_MOCK_DATA = {
  customer_info: {
    customer_id: 5500,
    participant_id: "5500",
    name: "Mike Johnson",
    initials: "MJ",
    email: "mike.johnson@example.com",
    age: 28,
    report_id: "MG5500",
    lab_name: "Lab_1 Diagnostics",
    upload_date: "2025-08-12",
    last_updated: "March 12, 2025"
  },

  // Domain-specific bacterial profiles for Mike Johnson
  // Mike has mixed results - good in some areas, concerning in others
  domain_bacteria: {
    aging: {
      bacteria: [
        {
          msp_id: "msp_aging_mj_01",
          bacteria_name: "Lactobacillus longum",
          full_name: "Lactobacillus longum BB536",
          abundance: 0.0000067891,                    // Raw database value
          current_level: "6.8 units",                 // ✅ Patient-friendly display
          percentage: 2.264,                          // % of optimal level (0-1 format)
          confidence_level: "A",
          status: "HIGH",
          optimal_range: [0.000002, 0.000004],
          category: "probiotic",
          description: "Anti-aging probiotic but elevated levels may indicate dysbiosis"
        },
        {
          msp_id: "msp_aging_mj_02",
          bacteria_name: "Bifidobacterium animalis",
          full_name: "Bifidobacterium animalis lactis",
          abundance: 0.0000045678,                    // Raw database value
          current_level: "4.6 units",                 // ✅ Patient-friendly display
          percentage: 2.284,                          // % of optimal level (0-1 format)
          confidence_level: "B",
          status: "HIGH",
          optimal_range: [0.000001, 0.000003],
          category: "probiotic",
          description: "Beneficial but overgrown, may crowd out other species"
        },
        {
          msp_id: "msp_aging_mj_03",
          bacteria_name: "Akkermansia muciniphila",
          full_name: "Akkermansia muciniphila",
          abundance: 0.0000023456,                    // Raw database value
          current_level: "7.8 units",                 // ✅ Patient-friendly display
          percentage: 0.782,                          // % of optimal level (0-1 format)
          confidence_level: "A",
          status: "NORMAL",
          optimal_range: [0.000002, 0.000004],
          category: "beneficial",
          description: "Optimal levels for longevity and metabolic health"
        },
        {
          msp_id: "msp_aging_mj_04",
          bacteria_name: "Lactobacillus helveticus",
          full_name: "Lactobacillus helveticus",
          abundance: 0.0000034567,                    // Raw database value
          current_level: "9.9 units",                 // ✅ Patient-friendly display
          percentage: 0.988,                          // % of optimal level (0-1 format)
          confidence_level: "A",
          status: "NORMAL",
          optimal_range: [0.000003, 0.000005],
          category: "probiotic",
          description: "Good levels for cognitive aging protection"
        }
      ],
      scores: {
        diversity: 3.2,
        overall: 3.6,
        status: "good"
      }
    },

    gut: {
      bacteria: [
        {
          msp_id: "msp_gut_mj_01",
          bacteria_name: "Bacteroides uniformis",
          full_name: "Bacteroides uniformis",
          abundance: 0.0000012345,                    // Raw database value
          current_level: "2.7 units",                 // ✅ Patient-friendly display
          percentage: 0.274,                          // % of optimal level (0-1 format)
          confidence_level: "C",
          status: "LOW",
          optimal_range: [0.000003, 0.000006],
          category: "beneficial",
          description: "Important for carbohydrate metabolism, levels too low"
        },
        {
          msp_id: "msp_gut_mj_02",
          bacteria_name: "Clostridium difficile",
          full_name: "Clostridium difficile",
          abundance: 0.0000056789,                    // Raw database value
          current_level: "18.9 units",                // ✅ Patient-friendly display (HIGH!)
          percentage: 18.930,                         // % of optimal level (0-1 format)
          confidence_level: "B",
          status: "HIGH",
          optimal_range: [0.0000001, 0.0000005],     // Very low optimal for pathogen
          category: "pathogen",
          description: "Concerning pathogen levels, potential for gut inflammation"
        },
        {
          msp_id: "msp_gut_mj_03",
          bacteria_name: "Lactobacillus brevis",
          full_name: "Lactobacillus brevis",
          abundance: 0.0000001234,                    // Raw database value
          current_level: "0.4 units",                 // ✅ Patient-friendly display
          percentage: 0.041,                          // % of optimal level (0-1 format)
          confidence_level: "C",
          status: "LOW",
          optimal_range: [0.000002, 0.000004],
          category: "probiotic",
          description: "Immune-supporting probiotic, levels insufficient"
        },
        {
          msp_id: "msp_gut_mj_04",
          bacteria_name: "Enterobacter cloacae",
          full_name: "Enterobacter cloacae",
          abundance: 0.0000034567,                    // Raw database value
          current_level: "4.6 units",                 // ✅ Patient-friendly display
          percentage: 4.609,                          // % of optimal level (0-1 format)
          confidence_level: "B",
          status: "HIGH",
          optimal_range: [0.0000005, 0.000001],
          category: "pathogen",
          description: "Opportunistic pathogen, elevated levels indicate gut dysbiosis"
        }
      ],
      scores: {
        diversity: 2.1,
        overall: 2.4,
        status: "poor"
      }
    },

    liver: {
      bacteria: [
        {
          msp_id: "msp_liver_mj_01",
          bacteria_name: "Lactobacillus rhamnosus",
          full_name: "Lactobacillus rhamnosus GG",
          abundance: 0.0000045678,                    // Raw database value
          current_level: "2.3 units",                 // ✅ Patient-friendly display
          percentage: 2.284,                          // % of optimal level (0-1 format)
          confidence_level: "A",
          status: "HIGH",
          optimal_range: [0.000001, 0.000003],
          category: "probiotic",
          description: "Liver-protective but overgrown, may indicate compensation"
        },
        {
          msp_id: "msp_liver_mj_02",
          bacteria_name: "Enterococcus faecium",
          full_name: "Enterococcus faecium",
          abundance: 0.0000001234,                    // Raw database value
          current_level: "0.6 units",                 // ✅ Patient-friendly display
          percentage: 0.617,                          // % of optimal level (0-1 format)
          confidence_level: "C",
          status: "NORMAL",
          optimal_range: [0.0000001, 0.0000003],
          category: "neutral",
          description: "Within normal range for liver function"
        },
        {
          msp_id: "msp_liver_mj_03",
          bacteria_name: "Bifidobacterium lactis",
          full_name: "Bifidobacterium lactis",
          abundance: 0.0000067891,                    // Raw database value
          current_level: "2.7 units",                 // ✅ Patient-friendly display
          percentage: 2.716,                          // % of optimal level (0-1 format)
          confidence_level: "B",
          status: "HIGH",
          optimal_range: [0.000002, 0.000004],
          category: "probiotic",
          description: "Beneficial for liver but elevated, suggests dysbiosis"
        },
        {
          msp_id: "msp_liver_mj_04",
          bacteria_name: "Lactobacillus delbrueckii",
          full_name: "Lactobacillus delbrueckii bulgaricus",
          abundance: 0.0000023456,                    // Raw database value
          current_level: "7.8 units",                 // ✅ Patient-friendly display
          percentage: 0.782,                          // % of optimal level (0-1 format)
          confidence_level: "B",
          status: "NORMAL",
          optimal_range: [0.000002, 0.000004],
          category: "probiotic",
          description: "Good levels for liver detoxification support"
        }
      ],
      scores: {
        diversity: 3.1,
        overall: 3.4,
        status: "good"
      }
    },

    heart: {
      bacteria: [
        {
          msp_id: "msp_heart_mj_01",
          bacteria_name: "Streptococcus mutans",
          full_name: "Streptococcus mutans",
          abundance: 0.0000078912,                    // Raw database value
          current_level: "26.3 units",                // ✅ Patient-friendly display (VERY HIGH!)
          percentage: 26.304,                         // % of optimal level (0-1 format)
          confidence_level: "B",
          status: "HIGH",
          optimal_range: [0.0000001, 0.0000005],
          category: "pathogen",
          description: "Oral pathogen, high levels increase cardiovascular risk"
        },
        {
          msp_id: "msp_heart_mj_02",
          bacteria_name: "Lactobacillus salivarius",
          full_name: "Lactobacillus salivarius",
          abundance: 0.0000012345,                    // Raw database value
          current_level: "3.1 units",                 // ✅ Patient-friendly display
          percentage: 0.309,                          // % of optimal level (0-1 format)
          confidence_level: "C",
          status: "LOW",
          optimal_range: [0.000003, 0.000005],
          category: "probiotic",
          description: "Cardio-protective probiotic, levels too low"
        }
      ],
      scores: {
        diversity: 2.3,
        overall: 2.7,
        status: "poor"
      }
    },

    skin: {
      bacteria: [
        {
          msp_id: "msp_skin_mj_01",
          bacteria_name: "Staphylococcus aureus",
          full_name: "Staphylococcus aureus",
          abundance: 0.0000056789,                    // Raw database value
          current_level: "28.4 units",                // ✅ Patient-friendly display (VERY HIGH!)
          percentage: 28.395,                         // % of optimal level (0-1 format)
          confidence_level: "B",
          status: "HIGH",
          optimal_range: [0.0000001, 0.0000003],
          category: "pathogen",
          description: "Skin pathogen, high levels indicate skin microbiome dysbiosis"
        },
        {
          msp_id: "msp_skin_mj_02",
          bacteria_name: "Cutibacterium acnes",
          full_name: "Cutibacterium acnes",
          abundance: 0.0000034567,                    // Raw database value
          current_level: "23.0 units",                // ✅ Patient-friendly display (HIGH)
          percentage: 2.305,                          // % of optimal level (0-1 format)
          confidence_level: "C",
          status: "HIGH",
          optimal_range: [0.000001, 0.000002],
          category: "concerning",
          description: "Acne-causing bacteria, elevated levels"
        },
        {
          msp_id: "msp_skin_mj_03",
          bacteria_name: "Lactobacillus plantarum",
          full_name: "Lactobacillus plantarum",
          abundance: 0.0000001234,                    // Raw database value
          current_level: "0.4 units",                 // ✅ Patient-friendly display
          percentage: 0.041,                          // % of optimal level (0-1 format)
          confidence_level: "C",
          status: "LOW",
          optimal_range: [0.000002, 0.000004],
          category: "probiotic",
          description: "Skin-protective probiotic, insufficient levels"
        }
      ],
      scores: {
        diversity: 2.4,
        overall: 2.1,
        status: "poor"
      }
    },

    cognitive: {
      bacteria: [
        {
          msp_id: "msp_brain_mj_01",
          bacteria_name: "Escherichia coli",
          full_name: "Escherichia coli",
          abundance: 0.0000045678,                    // Raw database value
          current_level: "30.5 units",                // ✅ Patient-friendly display (HIGH)
          percentage: 3.045,                          // % of optimal level (0-1 format)
          evidence_strength: "C",
          status: "HIGH",
          optimal_range: [0.000001, 0.000002],
          category: "concerning",
          description: "Elevated E. coli may produce neuroinflammatory compounds"
        },
        {
          msp_id: "msp_brain_mj_02",
          bacteria_name: "Lactobacillus helveticus",
          full_name: "Lactobacillus helveticus R0052",
          abundance: 0.0000012345,                    // Raw database value
          current_level: "3.5 units",                 // ✅ Patient-friendly display
          percentage: 0.353,                          // % of optimal level (0-1 format)
          confidence_level: "A",
          status: "LOW",
          optimal_range: [0.000003, 0.000005],
          category: "probiotic",
          description: "Psychobiotic strain, levels too low for optimal cognitive benefit"
        },
        {
          msp_id: "msp_brain_mj_03",
          bacteria_name: "Bifidobacterium longum",
          full_name: "Bifidobacterium longum 1714",
          abundance: 0.0000023456,                    // Raw database value
          current_level: "5.2 units",                 // ✅ Patient-friendly display
          percentage: 0.521,                          // % of optimal level (0-1 format)
          confidence_level: "A",
          status: "LOW",
          optimal_range: [0.000004, 0.000006],
          category: "probiotic",
          description: "Memory-enhancing strain, insufficient for cognitive support"
        }
      ],
      scores: {
        diversity: 2.8,
        overall: 2.5,
        status: "poor"
      }
    }
  },

  // Overall health metrics for Mike Johnson - Mixed results
  overall_health: {
    diversity_score: 2.7,
    overall_score: 2.9,
    status: "warning",
    total_bacteria_analyzed: 20,
    concerning_bacteria: 8,
    beneficial_bacteria: 9,
    neutral_bacteria: 3
  },

  // Clinical context and recommendations
  clinical_notes: {
    primary_concerns: [
      "High pathogenic bacteria in gut and skin domains",
      "Elevated Clostridium difficile poses infection risk",
      "Poor gut-brain axis function due to dysbiosis",
      "Cardiovascular risk from oral pathogens",
      "Skin microbiome imbalance"
    ],
    recommendations: [
      "Immediate probiotic intervention with multi-strain formula",
      "Eliminate refined sugars and processed foods",
      "Consider antimicrobial herbs under medical supervision",
      "Improve oral hygiene to reduce Streptococcus mutans",
      "Focus on prebiotic fiber to restore beneficial bacteria",
      "Stress management for gut-brain axis healing",
      "Consider fecal microbiota transplantation consultation"
    ]
  }
};

export default MIKE_JOHNSON_MOCK_DATA;