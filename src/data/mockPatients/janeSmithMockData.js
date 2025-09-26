// Mock Data for Jane Smith (Customer ID: 8420 / Participant ID: 8420)
// Patient-friendly current_level values instead of scientific notation

const JANE_SMITH_MOCK_DATA = {
  customer_info: {
    customer_id: 8420,
    participant_id: "8420",
    name: "Jane Smith",
    initials: "JS",
    email: "jane.smith@example.com",
    age: 32,
    report_id: "MG8420",
    lab_name: "Lab_3 Diagnostics",
    upload_date: "2025-08-12",
    last_updated: "March 12, 2025"
  },

  // Domain-specific bacterial profiles for Jane Smith
  // Jane has generally better bacterial balance compared to John
  domain_bacteria: {
    aging: {
      bacteria: [
        {
          msp_id: "msp_1138",
          bacteria_name: "Clostridium butyricum",
          full_name: "Clostridium butyricum CAG:628",
          abundance: 0.0000037011,                    // Raw database value
          current_level: "3.7 units",                 // ✅ Patient-friendly display
          percentage: 1.234,                          // % of optimal level (0-1 format)
          confidence_level: "C",
          status: "NORMAL",
          optimal_range: [0.000002, 0.000004],
          category: "beneficial",
          description: "Excellent butyrate producer, supports anti-aging pathways"
        },
        {
          msp_id: "msp_0491",
          bacteria_name: "Akkermansia muciniphila",
          full_name: "Akkermansia muciniphila",
          abundance: 0.0000009152,                    // Raw database value
          current_level: "1.4 units",                 // ✅ Patient-friendly display
          percentage: 0.915,                          // % of optimal level (0-1 format)
          confidence_level: "C",
          status: "NORMAL",
          optimal_range: [0.0000008, 0.000002],
          category: "beneficial",
          description: "Mucus layer maintenance, longevity-associated bacteria"
        },
        {
          msp_id: "msp_0452",
          bacteria_name: "Bifidobacterium animalis",
          full_name: "Bifidobacterium animalis",
          abundance: 0.0000006835,                    // Raw database value
          current_level: "0.9 units",                 // ✅ Patient-friendly display
          percentage: 0.911,                          // % of optimal level (0-1 format)
          confidence_level: "B",
          status: "NORMAL",
          optimal_range: [0.0000005, 0.000001],
          category: "probiotic",
          description: "Immune system support and healthy aging"
        },
        {
          msp_id: "msp_0632",
          bacteria_name: "Lactobacillus plantarum",
          full_name: "Lactobacillus plantarum",
          abundance: 0.0000000646,                    // Raw database value
          current_level: "0.3 units",                 // ✅ Patient-friendly display
          percentage: 0.323,                          // % of optimal level (0-1 format)
          confidence_level: "C",
          status: "LOW",
          optimal_range: [0.000001, 0.000003],
          category: "probiotic",
          description: "Antioxidant producer, cellular protection"
        }
      ],
      scores: {
        diversity: 3.8,
        overall: 4.2,
        status: "excellent"
      }
    },

    gut: {
      bacteria: [
        {
          msp_id: "msp_1576",
          bacteria_name: "Eggerthella lenta",
          full_name: "Eggerthella lenta",
          abundance: 0.0000006466,                    // Raw database value
          current_level: "0.9 units",                 // ✅ Patient-friendly display
          percentage: 0.862,                          // % of optimal level (0-1 format)
          confidence_level: "C",
          status: "NORMAL",
          optimal_range: [0.0000005, 0.000001],
          category: "beneficial",
          description: "Drug metabolism and gut health maintenance"
        },
        {
          msp_id: "msp_0933",
          bacteria_name: "Blautia wexlerae",
          full_name: "Blautia wexlerae",
          abundance: 0.0000002201,                    // Raw database value
          current_level: "0.7 units",                 // ✅ Patient-friendly display
          percentage: 0.734,                          // % of optimal level (0-1 format)
          confidence_level: "C",
          status: "NORMAL",
          optimal_range: [0.0000001, 0.0000005],
          category: "beneficial",
          description: "Short-chain fatty acid production"
        },
        {
          msp_id: "msp_0769",
          bacteria_name: "Agathobaculum butyriciproducens",
          full_name: "Agathobaculum butyriciproducens",
          abundance: 0.0000007216,                    // Raw database value
          current_level: "0.9 units",                 // ✅ Patient-friendly display
          percentage: 0.962,                          // % of optimal level (0-1 format)
          confidence_level: "A",
          status: "NORMAL",
          optimal_range: [0.0000006, 0.000001],
          category: "beneficial",
          description: "High butyrate producer, excellent for gut barrier"
        },
        {
          msp_id: "msp_1782",
          bacteria_name: "Prevotella melaninogenica",
          full_name: "Prevotella melaninogenica",
          abundance: 0.0000001321,                    // Raw database value
          current_level: "0.7 units",                 // ✅ Patient-friendly display
          percentage: 0.661,                          // % of optimal level (0-1 format)
          confidence_level: "C",
          status: "NORMAL",
          optimal_range: [0.0000001, 0.0000003],
          category: "beneficial",
          description: "Protein metabolism and gut health"
        }
      ],
      scores: {
        diversity: 4.1,
        overall: 4.3,
        status: "excellent"
      }
    },

    liver: {
      bacteria: [
        {
          msp_id: "msp_0070",
          bacteria_name: "Akkermansia muciniphila",
          full_name: "Akkermansia muciniphila type 2",
          abundance: 0.000000487,                     // Raw database value
          current_level: "0.9 units",                 // ✅ Patient-friendly display
          percentage: 0.876,                          // % of optimal level (0-1 format)
          confidence_level: "C",
          status: "NORMAL",
          optimal_range: [0.0000003, 0.0000008],
          category: "beneficial",
          description: "Liver protection and metabolic health"
        },
        {
          msp_id: "msp_1908",
          bacteria_name: "Lactobacillus casei",
          full_name: "Lactobacillus casei",
          abundance: 0.0000000717,                    // Raw database value
          current_level: "0.5 units",                 // ✅ Patient-friendly display
          percentage: 0.478,                          // % of optimal level (0-1 format)
          evidence_strength: "C",
          status: "LOW",
          optimal_range: [0.000001, 0.000002],
          category: "probiotic",
          description: "Liver detoxification support"
        },
        {
          msp_id: "msp_0030",
          bacteria_name: "Bifidobacterium breve",
          full_name: "Bifidobacterium breve",
          abundance: 0.0000037143,                    // Raw database value
          current_level: "1.9 units",                 // ✅ Patient-friendly display
          percentage: 1.857,                          // % of optimal level (0-1 format)
          confidence_level: "B",
          status: "HIGH",
          optimal_range: [0.000001, 0.000003],
          category: "probiotic",
          description: "Generally beneficial but elevated levels may indicate imbalance"
        }
      ],
      scores: {
        diversity: 3.9,
        overall: 4.0,
        status: "excellent"
      }
    },

    heart: {
      bacteria: [
        {
          msp_id: "msp_heart_01",
          bacteria_name: "Roseburia intestinalis",
          full_name: "Roseburia intestinalis",
          abundance: 0.0000023456,                    // Raw database value
          current_level: "7.8 units",                 // ✅ Patient-friendly display
          percentage: 0.782,                          // % of optimal level (0-1 format)
          confidence_level: "A",
          status: "NORMAL",
          optimal_range: [0.000002, 0.000004],
          category: "beneficial",
          description: "Anti-inflammatory, supports cardiovascular health"
        },
        {
          msp_id: "msp_heart_02",
          bacteria_name: "Bacteroides uniformis",
          full_name: "Bacteroides uniformis",
          abundance: 0.0000034567,                    // Raw database value
          current_level: "8.6 units",                 // ✅ Patient-friendly display
          percentage: 0.864,                          // % of optimal level (0-1 format)
          confidence_level: "B",
          status: "NORMAL",
          optimal_range: [0.000003, 0.000005],
          category: "beneficial",
          description: "Cholesterol metabolism and heart health"
        },
        {
          msp_id: "msp_heart_03",
          bacteria_name: "Lactobacillus reuteri",
          full_name: "Lactobacillus reuteri",
          abundance: 0.0000012345,                    // Raw database value
          current_level: "8.2 units",                 // ✅ Patient-friendly display
          percentage: 0.823,                          // % of optimal level (0-1 format)
          confidence_level: "A",
          status: "NORMAL",
          optimal_range: [0.000001, 0.000002],
          category: "probiotic",
          description: "Cholesterol-lowering probiotic strain"
        }
      ],
      scores: {
        diversity: 4.2,
        overall: 4.4,
        status: "excellent"
      }
    },

    skin: {
      bacteria: [
        {
          msp_id: "msp_skin_js_01",
          bacteria_name: "Lactobacillus paracasei",
          full_name: "Lactobacillus paracasei",
          abundance: 0.0000045678,                    // Raw database value
          current_level: "9.1 units",                 // ✅ Patient-friendly display
          percentage: 0.914,                          // % of optimal level (0-1 format)
          confidence_level: "A",
          status: "NORMAL",
          optimal_range: [0.000004, 0.000006],
          category: "probiotic",
          description: "Skin barrier support and anti-inflammatory"
        },
        {
          msp_id: "msp_skin_js_02",
          bacteria_name: "Staphylococcus hominis",
          full_name: "Staphylococcus hominis",
          abundance: 0.0000012891,                    // Raw database value
          current_level: "8.6 units",                 // ✅ Patient-friendly display
          percentage: 0.859,                          // % of optimal level (0-1 format)
          confidence_level: "B",
          status: "NORMAL",
          optimal_range: [0.000001, 0.000002],
          category: "beneficial",
          description: "Protective skin commensal"
        }
      ],
      scores: {
        diversity: 3.7,
        overall: 4.1,
        status: "excellent"
      }
    },

    cognitive: {
      bacteria: [
        {
          msp_id: "msp_brain_js_01",
          bacteria_name: "Lactobacillus helveticus",
          full_name: "Lactobacillus helveticus R0052",
          abundance: 0.0000034567,                    // Raw database value
          current_level: "9.9 units",                 // ✅ Patient-friendly display
          percentage: 0.988,                          // % of optimal level (0-1 format)
          confidence_level: "A",
          status: "NORMAL",
          optimal_range: [0.000003, 0.000005],
          category: "probiotic",
          description: "Proven psychobiotic, reduces anxiety and improves cognition"
        },
        {
          msp_id: "msp_brain_js_02",
          bacteria_name: "Bifidobacterium longum",
          full_name: "Bifidobacterium longum 1714",
          abundance: 0.0000045678,                    // Raw database value
          current_level: "10.1 units",                // ✅ Patient-friendly display
          percentage: 1.015,                          // % of optimal level (0-1 format)
          confidence_level: "A",
          status: "NORMAL",
          optimal_range: [0.000004, 0.000006],
          category: "probiotic",
          description: "Memory enhancement and stress resilience"
        },
        {
          msp_id: "msp_brain_js_03",
          bacteria_name: "Lactobacillus rhamnosus",
          full_name: "Lactobacillus rhamnosus GG",
          abundance: 0.0000023456,                    // Raw database value
          current_level: "7.8 units",                 // ✅ Patient-friendly display
          percentage: 0.782,                          // % of optimal level (0-1 format)
          confidence_level: "A",
          status: "NORMAL",
          optimal_range: [0.000002, 0.000004],
          category: "probiotic",
          description: "Mood regulation and cognitive support"
        }
      ],
      scores: {
        diversity: 4.5,
        overall: 4.6,
        status: "excellent"
      }
    }
  },

  // Overall health metrics for Jane Smith - Much better than John
  overall_health: {
    diversity_score: 4.0,
    overall_score: 4.3,
    status: "excellent",
    total_bacteria_analyzed: 18,
    concerning_bacteria: 1,
    beneficial_bacteria: 16,
    neutral_bacteria: 1
  },

  // Clinical context and recommendations
  clinical_notes: {
    primary_concerns: [
      "Slightly elevated Bifidobacterium breve in liver domain",
      "Could benefit from more Lactobacillus plantarum for aging"
    ],
    recommendations: [
      "Maintain current healthy diet and lifestyle",
      "Continue probiotic foods to sustain excellent bacterial balance",
      "Monitor liver-associated bacteria periodically",
      "Focus on stress management for continued cognitive health"
    ]
  }
};

export default JANE_SMITH_MOCK_DATA;