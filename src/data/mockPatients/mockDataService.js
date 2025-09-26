// Mock Data Service - Integrates all patient data with proper API structure
// Import the individual patient mock data files

import JOHN_DOE_MOCK_DATA from './johnDoeMockData.js';
import JANE_SMITH_MOCK_DATA from './janeSmithMockData.js';
import MIKE_JOHNSON_MOCK_DATA from './mikeJohnsonMockData.js';

class MockDataService {
  constructor() {
    // Map customer IDs to their mock data
    this.patientDatabase = {
      3091: JOHN_DOE_MOCK_DATA,     // John Doe - Poor health
      8420: JANE_SMITH_MOCK_DATA,   // Jane Smith - Excellent health
      5500: MIKE_JOHNSON_MOCK_DATA  // Mike Johnson - Mixed/Warning health
    };

    // Default fallback if customer not found
    this.defaultCustomer = 3091;
  }

  // Get customer info
  getCustomerInfo(customerId) {
    const customerData = this.patientDatabase[customerId] || this.patientDatabase[this.defaultCustomer];
    return customerData.customer_info;
  }

  // ✅ UPDATED: Get overall microbiome data for a customer (all domains combined) - NOW WITH RECOMMENDATIONS
  getCustomerMicrobiomeData(customerId) {
    const customerData = this.patientDatabase[customerId] || this.patientDatabase[this.defaultCustomer];
    const customerInfo = customerData.customer_info;
    const overallHealth = customerData.overall_health;

    // Combine bacteria from all domains for overall view
    let allBacteria = [];
    Object.keys(customerData.domain_bacteria).forEach(domain => {
      const domainBacteria = customerData.domain_bacteria[domain].bacteria.map(bacteria => ({
        ...bacteria,
        domain: domain
      }));
      allBacteria = allBacteria.concat(domainBacteria);
    });

    // Create species carousel for frontend
    const speciesCarousel = this.createSpeciesCarousel(allBacteria, "Overall Microbiome");

    // ✅ FIXED: Include recommendations from customer data
    const recommendations = customerData.recommendations || null;

    console.log(`🎯 MockDataService: Overall microbiome data for customer ${customerId} includes recommendations:`, !!recommendations);

    return {
      success: true,
      domain_info: {
        domain_id: "microbiome",
        domain_name: `Microbiome Analysis - ${customerInfo.name}`,
        description: `Comprehensive bacterial analysis for ${customerInfo.name} (Customer ${customerId})`,
        score: overallHealth.overall_score,
        diversity: overallHealth.diversity_score,
        status: overallHealth.status
      },
      health_metrics: [
        {
          label: "Overall Health Score",
          value: overallHealth.overall_score,
          unit: "score",
          description: `Overall microbiome health for ${customerInfo.name}`
        },
        {
          label: "Diversity Score",
          value: overallHealth.diversity_score,
          unit: "index",
          description: "Bacterial diversity and richness indicator"
        },
        {
          label: "Bacteria Analyzed",
          value: overallHealth.total_bacteria_analyzed,
          unit: "count",
          description: "Total number of bacteria species identified"
        },
        {
          label: "Concerning Bacteria",
          value: overallHealth.concerning_bacteria,
          unit: "count",
          description: "Number of bacteria with concerning levels"
        }
      ],
      species_carousel: speciesCarousel,
      recommendations: recommendations, // ✅ FIXED: Include recommendations
      clinical_notes: customerData.clinical_notes || null, // ✅ BONUS: Include clinical notes
      metadata: {
        customer_id: customerId,
        customer_name: customerInfo.name,
        participant_id: customerInfo.participant_id,
        lab_name: customerInfo.lab_name,
        upload_date: customerInfo.upload_date,
        total_bacteria_count: overallHealth.total_bacteria_analyzed,
        data_source: "MOCK_DATA_SERVICE_WITH_RECOMMENDATIONS"
      }
    };
  }

  // ✅ UPDATED: Get domain-specific bacteria for a customer - NOW WITH RECOMMENDATIONS
  getCustomerDomainBacteria(customerId, domain) {
    const customerData = this.patientDatabase[customerId] || this.patientDatabase[this.defaultCustomer];
    const customerInfo = customerData.customer_info;
    
    // Check if domain exists, fallback to gut if not
    const domainData = customerData.domain_bacteria[domain] || customerData.domain_bacteria.gut;
    
    if (!domainData) {
      return {
        success: false,
        error: `Domain '${domain}' not found for customer ${customerId}`
      };
    }

    // Create domain-specific species carousel
    const speciesCarousel = this.createSpeciesCarousel(
      domainData.bacteria, 
      `${domain.charAt(0).toUpperCase() + domain.slice(1)} Health`
    );

    // ✅ FIXED: Get recommendations from customer data
    const recommendations = customerData.recommendations || null;

    console.log(`🎯 MockDataService: Including recommendations for customer ${customerId}, domain ${domain}`);
    console.log('📋 Recommendations structure:', recommendations ? Object.keys(recommendations) : 'No recommendations');

    return {
      success: true,
      domain_info: {
        domain_id: domain,
        domain_name: `${domain.charAt(0).toUpperCase() + domain.slice(1)} Health - ${customerInfo.name}`,
        description: `Bacterial analysis for ${domain} health in ${customerInfo.name} (Customer ${customerId})`,
        score: domainData.scores.overall,
        diversity: domainData.scores.diversity,
        status: domainData.scores.status
      },
      health_metrics: [
        {
          label: `${domain.charAt(0).toUpperCase() + domain.slice(1)} Score`,
          value: domainData.scores.overall,
          unit: "score",
          description: `${domain} health score for ${customerInfo.name}`
        },
        {
          label: "Diversity",
          value: domainData.scores.diversity,
          unit: "index",
          description: `Bacterial diversity in ${domain} system`
        },
        {
          label: "Bacteria Count",
          value: domainData.bacteria.length,
          unit: "count",
          description: `Number of ${domain}-related bacteria analyzed`
        }
      ],
      species_carousel: speciesCarousel,
      recommendations: recommendations, // ✅ FIXED: Include recommendations here
      clinical_notes: customerData.clinical_notes || null, // ✅ BONUS: Include clinical notes
      metadata: {
        customer_id: customerId,
        customer_name: customerInfo.name,
        domain: domain,
        data_source: "PATIENT_DOMAIN_DATA_WITH_RECOMMENDATIONS"
      }
    };
  }

  // Create species carousel compatible with frontend
  createSpeciesCarousel(bacteriaList, title) {
    // Group bacteria by category
    const categories = {
      bacteria: {
        title: `${title} - Primary Bacteria`,
        status: this.calculateCategoryStatus(bacteriaList.filter(b => b.category === 'beneficial' || b.category === 'neutral')),
        species: []
      },
      probiotics: {
        title: `${title} - Probiotic Species`,
        status: this.calculateCategoryStatus(bacteriaList.filter(b => b.category === 'probiotic')),
        species: []
      },
      pathogens: {
        title: `${title} - Concerning Species`,
        status: this.calculateCategoryStatus(bacteriaList.filter(b => b.category === 'pathogen' || b.category === 'concerning')),
        species: []
      }
    };

    // Distribute bacteria into categories
    bacteriaList.forEach(bacteria => {
      const speciesInfo = {
        name: bacteria.bacteria_name,
        scientific_name: bacteria.full_name,
        current_level: bacteria.percentage,
        optimal_level: this.calculateOptimalPercentage(bacteria.optimal_range),
        range_min: bacteria.optimal_range[0].toExponential(2),
        range_max: bacteria.optimal_range[1].toExponential(2),
        measurement_unit: "relative abundance",
        status: bacteria.status.toLowerCase(),
        is_beneficial: bacteria.category === 'beneficial' || bacteria.category === 'probiotic',
        percentage: bacteria.percentage,
        range_fill_width: Math.min(100, bacteria.percentage * 0.8),
        marker_position: Math.min(100, bacteria.percentage * 0.85),
        msp_id: bacteria.msp_id,
        evidence_strength: bacteria.evidence_strength || bacteria.confidence_level,
        description: bacteria.description
      };

      // Categorize bacteria
      if (bacteria.category === 'probiotic') {
        categories.probiotics.species.push(speciesInfo);
      } else if (bacteria.category === 'pathogen' || bacteria.category === 'concerning') {
        categories.pathogens.species.push(speciesInfo);
      } else {
        categories.bacteria.species.push(speciesInfo);
      }
    });

    return categories;
  }

  // Calculate optimal percentage for display
  calculateOptimalPercentage(optimalRange) {
    const midpoint = (optimalRange[0] + optimalRange[1]) / 2;
    return midpoint * 1000; // Convert to percentage-like scale
  }

  // Calculate category status based on bacteria statuses
  calculateCategoryStatus(bacteriaList) {
    if (bacteriaList.length === 0) return "No Data";
    
    const statusCounts = {
      LOW: bacteriaList.filter(b => b.status === 'LOW').length,
      HIGH: bacteriaList.filter(b => b.status === 'HIGH').length,
      NORMAL: bacteriaList.filter(b => b.status === 'NORMAL').length
    };

    const total = bacteriaList.length;
    const normalRatio = statusCounts.NORMAL / total;

    if (normalRatio >= 0.8) return "Excellent";
    if (normalRatio >= 0.6) return "Good";
    if (normalRatio >= 0.4) return "Fair";
    return "Poor";
  }

  // Get user profile information
  getUserProfile(customerId) {
    const customerData = this.patientDatabase[customerId] || this.patientDatabase[this.defaultCustomer];
    const customerInfo = customerData.customer_info;

    return {
      success: true,
      user: {
        user_id: customerId,
        customer_id: customerId,
        username: customerInfo.name.toLowerCase().replace(' ', '.'),
        email: customerInfo.email,
        first_name: customerInfo.name.split(' ')[0],
        last_name: customerInfo.name.split(' ')[1] || '',
        full_name: customerInfo.name,
        initials: customerInfo.initials,
        report_id: customerInfo.report_id,
        created_at: "January 15, 2024",
        last_updated: customerInfo.last_updated,
        status: "active",
        age: customerInfo.age
      }
    };
  }

  // Test endpoint to show customer differences
  getCustomerDifferences() {
    const results = {};
    
    Object.keys(this.patientDatabase).forEach(customerId => {
      const customerData = this.patientDatabase[customerId];
      const customerInfo = customerData.customer_info;
      const overallHealth = customerData.overall_health;
      const agingData = customerData.domain_bacteria.aging;
      
      results[`customer_${customerId}`] = {
        name: customerInfo.name,
        overall_score: overallHealth.overall_score,
        overall_status: overallHealth.status,
        aging_score: agingData.scores.overall,
        aging_status: agingData.scores.status,
        aging_bacteria_count: agingData.bacteria.length,
        aging_top_bacteria: agingData.bacteria[0]?.bacteria_name || "No data",
        concerning_bacteria_count: overallHealth.concerning_bacteria,
        total_bacteria: overallHealth.total_bacteria_analyzed
      };
    });

    return {
      success: true,
      message: "Customer differences test - each customer shows unique bacterial profiles",
      available_customers: Object.keys(this.patientDatabase).map(id => parseInt(id)),
      results: results
    };
  }

  // Get clinical notes and recommendations
  getCustomerClinicalNotes(customerId) {
    const customerData = this.patientDatabase[customerId] || this.patientDatabase[this.defaultCustomer];
    return {
      success: true,
      clinical_notes: customerData.clinical_notes,
      customer_name: customerData.customer_info.name
    };
  }

  // ✅ NEW: Get customer-specific recommendations
  getCustomerRecommendations(customerId, domain = null) {
    const customerData = this.patientDatabase[customerId] || this.patientDatabase[this.defaultCustomer];
    
    // Check if the customer data has recommendations
    if (customerData.recommendations) {
      console.log(`📋 Found recommendations for customer ${customerId}`);
      return customerData.recommendations;
    }

    console.log(`⚠️ No recommendations found for customer ${customerId}, using default`);
    // ✅ FALLBACK: Return domain-specific default recommendations
    return this.getDefaultRecommendationsForDomain(domain || 'gut');
  }

  // ✅ NEW: Default recommendations per domain (fallback)
  getDefaultRecommendationsForDomain(domain) {
    const domainRecommendations = {
      aging: {
        probiotics: [
          {
            name: "Lactobacillus longum",
            description: "Anti-aging probiotic strain",
            dosage: "10 billion CFU daily",
            duration: "3 months",
            reason: "Support longevity pathways",
            evidence_level: "strong",
            priority: 1,
            recommended: true
          }
        ],
        supplements: [
          {
            name: "Resveratrol",
            description: "Antioxidant for cellular aging",
            dosage: "500mg daily",
            duration: "Ongoing",
            reason: "Combat oxidative stress",
            evidence_level: "moderate",
            priority: 2,
            recommended: true
          }
        ],
        diet: [
          {
            name: "Antioxidant-Rich Foods",
            description: "Berries, dark chocolate, green tea",
            dosage: "Daily intake",
            duration: "Ongoing",
            reason: "Support anti-aging pathways",
            evidence_level: "strong",
            priority: 1,
            recommended: true
          }
        ],
        lifestyle: [
          {
            name: "Regular Exercise",
            description: "Moderate cardio and strength training",
            dosage: "30 min daily",
            duration: "Ongoing",
            reason: "Promote cellular health",
            evidence_level: "strong",
            priority: 1,
            recommended: true
          }
        ]
      },
      
      liver: {
        probiotics: [
          {
            name: "Lactobacillus rhamnosus",
            description: "Liver-protective strain",
            dosage: "15 billion CFU daily",
            duration: "4 months",
            reason: "Support liver detoxification",
            evidence_level: "strong",
            priority: 1,
            recommended: true
          }
        ],
        supplements: [
          {
            name: "Milk Thistle",
            description: "Liver regeneration support",
            dosage: "300mg twice daily",
            duration: "3 months",
            reason: "Protect liver cells",
            evidence_level: "strong",
            priority: 1,
            recommended: true
          }
        ],
        diet: [
          {
            name: "Cruciferous Vegetables",
            description: "Broccoli, kale, Brussels sprouts",
            dosage: "2-3 servings daily",
            duration: "Ongoing",
            reason: "Support detox pathways",
            evidence_level: "strong",
            priority: 1,
            recommended: true
          }
        ],
        lifestyle: [
          {
            name: "Reduce Alcohol",
            description: "Limit alcohol consumption",
            dosage: "Max 1 drink/day",
            duration: "Ongoing",
            reason: "Reduce liver burden",
            evidence_level: "strong",
            priority: 1,
            recommended: true
          }
        ]
      },

      gut: {
        probiotics: [
          {
            name: "Multi-Strain Probiotic",
            description: "Comprehensive gut support",
            dosage: "50 billion CFU daily",
            duration: "6 months",
            reason: "Restore gut balance",
            evidence_level: "strong",
            priority: 1,
            recommended: true
          }
        ],
        supplements: [
          {
            name: "L-Glutamine",
            description: "Gut lining repair",
            dosage: "5g daily",
            duration: "3 months",
            reason: "Heal leaky gut",
            evidence_level: "strong",
            priority: 1,
            recommended: true
          }
        ],
        diet: [
          {
            name: "Fermented Foods",
            description: "Kefir, kimchi, sauerkraut",
            dosage: "Daily servings",
            duration: "Ongoing",
            reason: "Natural probiotic sources",
            evidence_level: "strong",
            priority: 1,
            recommended: true
          }
        ],
        lifestyle: [
          {
            name: "Stress Management",
            description: "Meditation, yoga",
            dosage: "20 min daily",
            duration: "Ongoing",
            reason: "Support gut-brain axis",
            evidence_level: "moderate",
            priority: 2,
            recommended: true
          }
        ]
      },

      cognitive: {
        probiotics: [
          {
            name: "Lactobacillus helveticus",
            description: "Psychobiotic for brain health",
            dosage: "10 billion CFU daily",
            duration: "4 months",
            reason: "Support cognitive function",
            evidence_level: "moderate",
            priority: 1,
            recommended: true
          }
        ],
        supplements: [
          {
            name: "Omega-3 DHA",
            description: "Brain health support",
            dosage: "1000mg daily",
            duration: "Ongoing",
            reason: "Support neural function",
            evidence_level: "strong",
            priority: 1,
            recommended: true
          }
        ],
        diet: [
          {
            name: "Brain Foods",
            description: "Fatty fish, nuts, blueberries",
            dosage: "Daily intake",
            duration: "Ongoing",
            reason: "Nourish brain tissue",
            evidence_level: "strong",
            priority: 1,
            recommended: true
          }
        ],
        lifestyle: [
          {
            name: "Mental Exercise",
            description: "Reading, puzzles, learning",
            dosage: "30 min daily",
            duration: "Ongoing",
            reason: "Maintain cognitive function",
            evidence_level: "strong",
            priority: 1,
            recommended: true
          }
        ]
      },

      heart: {
        probiotics: [
          {
            name: "Lactobacillus plantarum",
            description: "Cardiovascular support",
            dosage: "10 billion CFU daily",
            duration: "6 months",
            reason: "Support heart health",
            evidence_level: "moderate",
            priority: 2,
            recommended: true
          }
        ],
        supplements: [
          {
            name: "CoQ10",
            description: "Heart muscle support",
            dosage: "100mg daily",
            duration: "Ongoing",
            reason: "Energy production",
            evidence_level: "strong",
            priority: 1,
            recommended: true
          }
        ],
        diet: [
          {
            name: "Heart-Healthy Foods",
            description: "Olive oil, nuts, fish",
            dosage: "Daily intake",
            duration: "Ongoing",
            reason: "Support cardiovascular health",
            evidence_level: "strong",
            priority: 1,
            recommended: true
          }
        ],
        lifestyle: [
          {
            name: "Cardio Exercise",
            description: "Walking, swimming, cycling",
            dosage: "150 min/week",
            duration: "Ongoing",
            reason: "Strengthen heart",
            evidence_level: "strong",
            priority: 1,
            recommended: true
          }
        ]
      },

      skin: {
        probiotics: [
          {
            name: "Lactobacillus reuteri",
            description: "Skin health support",
            dosage: "5 billion CFU daily",
            duration: "3 months",
            reason: "Support skin microbiome",
            evidence_level: "moderate",
            priority: 2,
            recommended: true
          }
        ],
        supplements: [
          {
            name: "Collagen Peptides",
            description: "Skin structure support",
            dosage: "10g daily",
            duration: "3 months",
            reason: "Maintain skin elasticity",
            evidence_level: "moderate",
            priority: 1,
            recommended: true
          }
        ],
        diet: [
          {
            name: "Vitamin C Foods",
            description: "Citrus, berries, peppers",
            dosage: "Daily intake",
            duration: "Ongoing",
            reason: "Collagen synthesis",
            evidence_level: "strong",
            priority: 1,
            recommended: true
          }
        ],
        lifestyle: [
          {
            name: "Sun Protection",
            description: "SPF 30+ sunscreen daily",
            dosage: "Daily application",
            duration: "Ongoing",
            reason: "Prevent skin damage",
            evidence_level: "strong",
            priority: 1,
            recommended: true
          }
        ]
      }
    };

    return domainRecommendations[domain] || domainRecommendations.gut;
  }

  // ✅ NEW: Debug method to check recommendations
  debugCustomerRecommendations(customerId) {
    const customerData = this.patientDatabase[customerId] || this.patientDatabase[this.defaultCustomer];
    
    return {
      success: true,
      customer_id: customerId,
      customer_name: customerData.customer_info.name,
      has_recommendations: !!customerData.recommendations,
      recommendation_categories: customerData.recommendations ? Object.keys(customerData.recommendations) : [],
      recommendation_counts: customerData.recommendations ? Object.keys(customerData.recommendations).reduce((acc, category) => {
        acc[category] = customerData.recommendations[category].length;
        return acc;
      }, {}) : {},
      sample_recommendation: customerData.recommendations ? 
        customerData.recommendations.probiotics?.[0] || 
        customerData.recommendations.supplements?.[0] || 
        "No sample available" : null
    };
  }
}

// Export singleton instance
const mockDataService = new MockDataService();
export default mockDataService;