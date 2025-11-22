// Mobile Navigation Toggle
const hamburger = document.querySelector('.hamburger');
const navMenu = document.querySelector('.nav-menu');

if (hamburger && navMenu) {
    hamburger.addEventListener('click', () => {
        hamburger.classList.toggle('active');
        navMenu.classList.toggle('active');
    });

    // Close mobile menu when clicking on a link
    document.querySelectorAll('.nav-link').forEach(n => n.addEventListener('click', () => {
        hamburger.classList.remove('active');
        navMenu.classList.remove('active');
    }));
}

// Smooth scrolling for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Navbar background change on scroll
window.addEventListener('scroll', () => {
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        if (window.scrollY > 100) {
            navbar.style.background = 'rgba(255, 255, 255, 0.98)';
            navbar.style.boxShadow = '0 2px 20px rgba(0, 0, 0, 0.1)';
        } else {
            navbar.style.background = 'rgba(255, 255, 255, 0.95)';
            navbar.style.boxShadow = 'none';
        }
    }
});

// Scroll animations
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('visible');
        }
    });
}, observerOptions);

// Observe all sections for animation
document.querySelectorAll('section').forEach(section => {
    section.classList.add('fade-in');
    observer.observe(section);
});

// Form submission handling
const contactForm = document.querySelector('.contact-form');
if (contactForm) {
    contactForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Get form data
        const formData = new FormData(this);
        const name = formData.get('name');
        const email = formData.get('email');
        const message = formData.get('message');
        
        // Simple validation
        if (!name || !email || !message) {
            showNotification('Please fill in all fields', 'error');
            return;
        }
        
        if (!isValidEmail(email)) {
            showNotification('Please enter a valid email address', 'error');
            return;
        }
        
        // Simulate form submission
        showNotification('Message sent successfully!', 'success');
        this.reset();
    });
}

// Email validation function
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// API Configuration
const API_BASE_URL = '';

// API Helper Functions
async function apiCall(endpoint, data = null, method = 'GET') {
    try {
        const options = {
            method: method,
            headers: {
                'Content-Type': 'application/json',
            }
        };
        
        if (data && (method === 'POST' || method === 'PUT')) {
            options.body = JSON.stringify(data);
        }
        
        const response = await fetch(`${API_BASE_URL}${endpoint}`, options);
        const result = await response.json();
        
        if (!response.ok) {
            throw new Error(result.error || 'API request failed');
        }
        
        return result;
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

// Investment Analysis Functions
async function analyzeFixedDeposits() {
    try {
        const result = await apiCall('/api/investment/analyze', {
            type: 'fixed_deposits'
        }, 'POST');
        
        if (result.success) {
            displayInvestmentResults(result.data, 'Fixed Deposits');
        }
    } catch (error) {
        showNotification('Error analyzing fixed deposits: ' + error.message, 'error');
    }
}

async function analyzeEquity() {
    try {
        const result = await apiCall('/api/investment/analyze', {
            type: 'equity'
        }, 'POST');
        
        if (result.success) {
            displayInvestmentResults(result.data, 'Equity Markets');
        }
    } catch (error) {
        showNotification('Error analyzing equity markets: ' + error.message, 'error');
    }
}

function displayInvestmentResults(data, type) {
    // Create results display
    const resultsContainer = document.createElement('div');
    resultsContainer.className = 'investment-results';
    resultsContainer.innerHTML = `
        <h3>${type} Analysis Results</h3>
        <div class="results-table">
            <table>
                <thead>
                    <tr>
                        <th>Category</th>
                        <th>CAGR (%)</th>
                        <th>Volatility (%)</th>
                        <th>Risk Level</th>
                        <th>Liquidity</th>
                    </tr>
                </thead>
                <tbody>
                    ${data.map(item => `
                        <tr>
                            <td>${item.Subcategory || item.Sector || 'N/A'}</td>
                            <td>${item['CAGR (%)']?.toFixed(2) || 'N/A'}</td>
                            <td>${item['Volatility (%)']?.toFixed(2) || 'N/A'}</td>
                            <td>${item.Risk_Level || 'N/A'}</td>
                            <td>${item.Liquidity_Level?.toFixed(2) || 'N/A'}</td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        </div>
    `;
    
    // Display results (you can modify this to show in a modal or specific section)
    const targetSection = document.querySelector('#tools');
    if (targetSection) {
        const existingResults = targetSection.querySelector('.investment-results');
        if (existingResults) {
            existingResults.remove();
        }
        targetSection.appendChild(resultsContainer);
    }
}

// Budget Optimization Functions
async function optimizeBudget(budgetData) {
    try {
        const result = await apiCall('/api/budget/optimize', budgetData, 'POST');
        
        if (result.success) {
            displayBudgetResults(result);
        }
    } catch (error) {
        showNotification('Error optimizing budget: ' + error.message, 'error');
    }
}

function displayBudgetResults(result) {
    const { optimized_budget, analysis, goal_progress } = result;
    
    // Create budget results display
    const resultsContainer = document.createElement('div');
    resultsContainer.className = 'budget-results';
    resultsContainer.innerHTML = `
        <h3>Budget Optimization Results</h3>
        <div class="budget-summary">
            <div class="summary-item">
                <span class="label">Total Income:</span>
                <span class="value">₹${analysis.total_income.toLocaleString()}</span>
            </div>
            <div class="summary-item">
                <span class="label">Savings Rate:</span>
                <span class="value">${analysis.savings_rate_percent.toFixed(1)}%</span>
            </div>
            <div class="summary-item">
                <span class="label">Debt Ratio:</span>
                <span class="value">${analysis.debt_ratio_percent.toFixed(1)}%</span>
            </div>
        </div>
        <div class="budget-breakdown">
            <h4>Optimized Budget Allocation</h4>
            <div class="budget-chart">
                ${Object.entries(optimized_budget).map(([category, amount]) => `
                    <div class="budget-item">
                        <span class="category">${category}</span>
                        <span class="amount">₹${amount.toLocaleString()}</span>
                        <div class="bar" style="width: ${(amount / analysis.total_income) * 100}%"></div>
                    </div>
                `).join('')}
            </div>
        </div>
        <div class="recommendations">
            <h4>Recommendations</h4>
            <ul>
                ${analysis.recommendations.map(rec => `<li>${rec}</li>`).join('')}
            </ul>
        </div>
    `;
    
    // Display results
    const targetSection = document.querySelector('#tools');
    if (targetSection) {
        const existingResults = targetSection.querySelector('.budget-results');
        if (existingResults) {
            existingResults.remove();
        }
        targetSection.appendChild(resultsContainer);
    }
}

// Portfolio Optimization Functions
async function optimizePortfolio(portfolioData) {
    try {
        const result = await apiCall('/api/portfolio/optimize', portfolioData, 'POST');
        
        if (result.success) {
            displayPortfolioResults(result.results);
        }
    } catch (error) {
        showNotification('Error optimizing portfolio: ' + error.message, 'error');
    }
}

function displayPortfolioResults(results) {
    const resultsContainer = document.createElement('div');
    resultsContainer.className = 'portfolio-results';
    resultsContainer.innerHTML = `
        <h3>Portfolio Optimization Results</h3>
        <div class="portfolio-summary">
            <div class="summary-item">
                <span class="label">Required Return:</span>
                <span class="value">${results.required_return_percent?.toFixed(2)}%</span>
            </div>
            <div class="summary-item">
                <span class="label">Expected CAGR:</span>
                <span class="value">${results.portfolio_cagr_percent?.toFixed(2)}%</span>
            </div>
            <div class="summary-item">
                <span class="label">Portfolio Volatility:</span>
                <span class="value">${results.portfolio_volatility_percent?.toFixed(2)}%</span>
            </div>
        </div>
        <div class="asset-allocation">
            <h4>Asset Allocation</h4>
            <div class="allocation-chart">
                ${Object.entries(results.asset_allocation).map(([asset, allocation]) => `
                    <div class="allocation-item">
                        <span class="asset">${asset}</span>
                        <span class="allocation">${allocation.toFixed(1)}%</span>
                        <div class="bar" style="width: ${allocation}%"></div>
                    </div>
                `).join('')}
            </div>
        </div>
        <div class="projections">
            <h4>Projections</h4>
            <div class="projection-item">
                <span class="label">Projected Value:</span>
                <span class="value">₹${results.projected_nominal_value?.toLocaleString() || 'N/A'}</span>
            </div>
            <div class="projection-item">
                <span class="label">Stress Test Impact:</span>
                <span class="value">${results.stress_test_percent?.toFixed(1)}%</span>
            </div>
        </div>
        <div class="recommendations">
            <h4>Recommendations</h4>
            <ul>
                ${results.recommendations.map(rec => `<li>${rec}</li>`).join('')}
            </ul>
        </div>
    `;
    
    // Display results
    const targetSection = document.querySelector('#tools');
    if (targetSection) {
        const existingResults = targetSection.querySelector('.portfolio-results');
        if (existingResults) {
            existingResults.remove();
        }
        targetSection.appendChild(resultsContainer);
    }
}

// Enhanced Chatbot Functions
async function sendChatbotMessage() {
    const input = document.getElementById('chatbotInput');
    if (!input) return;
    
    const message = input.value.trim();
    
    if (message) {
        addChatbotMessage(message, 'user');
        input.value = '';
        
        try {
            const modeSelect = document.getElementById('aiModeSelect');
            const aiMode = (modeSelect && modeSelect.value) || 'ollama'; // 'ollama' | 'classic'
            let backendUsed = 'Classic';
            let result = null;

            if (aiMode === 'ollama') {
                try {
                    result = await apiCall('/api/chatbot/ollama', { message }, 'POST');
                    if (result && result.success && result.response) {
                        backendUsed = 'Ollama';
                        const container = document.getElementById('chatbotMessages');
                        if (container && result.response.length > 400) {
                            simulateStreaming(container, result.response, 'bot');
                        } else {
                addChatbotMessage(result.response, 'bot');
                        }
                        updateAiBackendBadge(backendUsed);
                        return;
                    }
                } catch (e) {
                    // fall through to classic
                }
                // fallback to classic
                result = await apiCall('/api/chatbot/query', { message }, 'POST');
                if (result.success) {
                    backendUsed = 'Classic';
                    const container = document.getElementById('chatbotMessages');
                    if (container && result.response && result.response.length > 400) {
                        simulateStreaming(container, result.response, 'bot');
                    } else {
                        addChatbotMessage(result.response || 'Okay.', 'bot');
                    }
                    updateAiBackendBadge(backendUsed);
                if (result.suggestions && result.suggestions.length > 0) {
                    addChatbotSuggestions(result.suggestions);
                }
            } else {
                addChatbotMessage('Sorry, I encountered an error. Please try again.', 'bot');
                }
            } else {
                // classic preferred
                try {
                    result = await apiCall('/api/chatbot/query', { message }, 'POST');
                    if (result && result.success) {
                        backendUsed = 'Classic';
                        const container = document.getElementById('chatbotMessages');
                        if (container && result.response && result.response.length > 400) {
                            simulateStreaming(container, result.response, 'bot');
                        } else {
                            addChatbotMessage(result.response || 'Okay.', 'bot');
                        }
                        updateAiBackendBadge(backendUsed);
                        if (result.suggestions && result.suggestions.length > 0) {
                            addChatbotSuggestions(result.suggestions);
                        }
                        return;
                    }
                } catch (e) {
                    // fall through to ollama
                }
                // fallback to ollama
                result = await apiCall('/api/chatbot/ollama', { message }, 'POST');
                if (result && result.success && result.response) {
                    backendUsed = 'Ollama';
                    const container = document.getElementById('chatbotMessages');
                    if (container && result.response.length > 400) {
                        simulateStreaming(container, result.response, 'bot');
                    } else {
                        addChatbotMessage(result.response, 'bot');
                    }
                    updateAiBackendBadge(backendUsed);
                } else {
                    addChatbotMessage('Sorry, I encountered an error. Please try again.', 'bot');
                }
            }
        } catch (error) {
            // Fallback to local responses if API fails
            const aiResponse = generateAIResponse(message);
            const container = document.getElementById('chatbotMessages');
            if (container && aiResponse.length > 400) {
                simulateStreaming(container, aiResponse, 'bot');
            } else {
            addChatbotMessage(aiResponse, 'bot');
            }
            updateAiBackendBadge('Local');
        }
    }
}

function addChatbotSuggestions(suggestions) {
    const messagesContainer = document.getElementById('chatbotMessages');
    if (!messagesContainer) return;
    
    const suggestionsDiv = document.createElement('div');
    suggestionsDiv.className = 'chatbot-suggestions';
    suggestionsDiv.innerHTML = `
        <p>You might also want to ask about:</p>
        <div class="suggestion-buttons">
            ${suggestions.map(suggestion => `
                <button class="suggestion-btn" onclick="askSuggestion('${suggestion}')">${suggestion}</button>
            `).join('')}
        </div>
    `;
    
    messagesContainer.appendChild(suggestionsDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function askSuggestion(suggestion) {
    const input = document.getElementById('chatbotInput');
    if (input) {
        input.value = suggestion;
        sendChatbotMessage();
    }
}

// Chatbot functionality
function openChatbot() {
    const modal = document.getElementById('chatbotModal');
    if (modal) {
        modal.style.display = 'block';
        // Ensure AI mode control is present
        ensureAiModeControl();
        // Focus on input
        setTimeout(() => {
            const input = document.getElementById('chatbotInput') || document.getElementById('dashboardChatbotInput');
            if (input) input.focus();
        }, 100);
    }
}

function closeChatbot() {
    const modal = document.getElementById('chatbotModal');
    if (modal) {
        modal.style.display = 'none';
    }
}

function handleChatbotInput(event) {
    if (event.key === 'Enter') {
        sendChatbotMessage();
    }
}

function addChatbotMessage(message, sender) {
    const messagesContainer = document.getElementById('chatbotMessages');
    if (!messagesContainer) return;
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;
    messageDiv.innerHTML = `<p>${renderMarkdownBasic(message)}</p>`;
    messagesContainer.appendChild(messageDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
    persistChatHistory(messagesContainer);
}

// Inject AI mode selector into chatbot header if not present
function ensureAiModeControl() {
    const header = document.querySelector('.chatbot-header');
    if (!header || document.getElementById('aiModeSelect')) return;
    const wrapper = document.createElement('div');
    wrapper.style.display = 'flex';
    wrapper.style.alignItems = 'center';
    wrapper.style.gap = '8px';
    wrapper.style.marginLeft = 'auto';
    wrapper.innerHTML = `
        <label for="aiModeSelect" style="font-size: 0.85rem; color: var(--text-secondary);">AI mode</label>
        <select id="aiModeSelect" style="padding: 6px 10px; border: 1px solid var(--border-color); border-radius: 8px; background: var(--card-bg); color: var(--text-primary);">
            <option value="ollama">Ollama</option>
            <option value="classic">Classic</option>
        </select>
        <span id="aiBackendBadge" style="font-size: 0.75rem; padding: 4px 8px; border-radius: 999px; background: #eef2ff; color: #4f46e5;">—</span>
    `;
    header.appendChild(wrapper);
}

function updateAiBackendBadge(label) {
    const badge = document.getElementById('aiBackendBadge');
    if (!badge) return;
    badge.textContent = label;
    if (label === 'Ollama') {
        badge.style.background = '#ecfdf5';
        badge.style.color = '#065f46';
    } else if (label === 'Classic') {
        badge.style.background = '#eff6ff';
        badge.style.color = '#1e40af';
    } else {
        badge.style.background = '#f3f4f6';
        badge.style.color = '#374151';
    }
}

function generateAIResponse(userMessage) {
    const responses = {
        'save money': 'To save more money, try the 50/30/20 rule: 50% for needs, 30% for wants, 20% for savings. Also, automate your savings and track all expenses.',
        'investment': 'Good investment options include mutual funds, fixed deposits, government bonds, and gold ETFs. Your choice depends on risk tolerance and time horizon.',
        'budget': 'Create a budget by tracking income, categorizing expenses, setting spending limits, and reviewing monthly. Use our Budget Optimizer tool for detailed analysis.',
        'emergency fund': 'Aim for 3-6 months of expenses in your emergency fund. Start small and build gradually. Keep it in a separate, easily accessible account.',
        'mutual fund': 'Mutual funds are a great way to invest in the stock market with professional management. Consider index funds for lower fees and better returns.',
        'tax': 'Tax-saving investments include ELSS, PPF, and NPS. Consult a tax advisor for personalized advice based on your income bracket.',
        'insurance': 'Life insurance should cover 10-15 times your annual income. Health insurance is essential for medical emergencies.',
        'retirement': 'Start retirement planning early. Use our Investment Guide tool to create a personalized retirement strategy.',
        'debt': 'Focus on paying high-interest debt first (credit cards, personal loans). Consider debt consolidation for better rates.',
        'credit score': 'Maintain a good credit score by paying bills on time, keeping credit utilization low, and avoiding too many credit inquiries.'
    };
    
    const lowerMessage = userMessage.toLowerCase();
    for (const [key, response] of Object.entries(responses)) {
        if (lowerMessage.includes(key)) {
            return response;
        }
    }
    
    // Default responses for common financial topics
    if (lowerMessage.includes('how') || lowerMessage.includes('what') || lowerMessage.includes('why')) {
        return "I'd be happy to help with your financial question. Could you please provide more specific details about what you'd like to know? You can also try asking about saving money, investments, budgeting, or insurance.";
    }
    
    if (lowerMessage.includes('hello') || lowerMessage.includes('hi') || lowerMessage.includes('hey')) {
        return "Hello! I'm your AI financial assistant. I can help you with questions about personal finance, investments, budgeting, and financial planning. What would you like to know?";
    }
    
    return "I understand you're asking about finances. For specific advice, try asking about topics like saving money, investments, budgeting, insurance, or retirement planning. How can I help you today?";
}

// Close chatbot when clicking outside
document.addEventListener('click', (e) => {
    const modal = document.getElementById('chatbotModal');
    if (modal && e.target === modal) {
        closeChatbot();
    }
});

// Notification system
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    // Show notification
    setTimeout(() => notification.classList.add('show'), 100);
    
    // Hide and remove notification
                setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// ================
// Chatbot UX extras
// ================

function escapeHtml(unsafe) {
    return String(unsafe)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;');
}

function renderMarkdownBasic(text) {
    // very lightweight renderer: bold, italics, code, links, line breaks
    let html = escapeHtml(text);
    html = html.replace(/`([^`]+)`/g, '<code>$1</code>');
    html = html.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
    html = html.replace(/\*([^*]+)\*/g, '<em>$1</em>');
    html = html.replace(/\[([^\]]+)\]\((https?:\/\/[^\s)]+)\)/g, '<a href="$2" target="_blank" rel="noopener">$1</a>');
    html = html.replace(/\n/g, '<br>');
    return html;
}

function simulateStreaming(containerEl, fullText, sender = 'bot', chunkSize = 30, delayMs = 30) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;
    const p = document.createElement('p');
    messageDiv.appendChild(p);
    containerEl.appendChild(messageDiv);
    containerEl.scrollTop = containerEl.scrollHeight;

    let index = 0;
    function tick() {
        const slice = fullText.slice(index, index + chunkSize);
        index += chunkSize;
        p.innerHTML = renderMarkdownBasic(fullText.slice(0, index));
        containerEl.scrollTop = containerEl.scrollHeight;
        if (index < fullText.length) {
            setTimeout(tick, delayMs);
        } else {
            persistChatHistory(containerEl);
        }
    }
    tick();
}

function persistChatHistory(containerEl) {
    try {
        const messages = [];
        containerEl.querySelectorAll('.message').forEach(m => {
            const role = m.classList.contains('user-message') ? 'user' : 'assistant';
            const content = m.textContent || '';
            messages.push({ role, content });
        });
        localStorage.setItem('chatHistory', JSON.stringify(messages));
    } catch (e) {}
}

function restoreChatHistory() {
    const container = document.getElementById('chatbotMessages');
    if (!container) return;
    try {
        const raw = localStorage.getItem('chatHistory');
        if (!raw) return;
        const messages = JSON.parse(raw);
        if (!Array.isArray(messages)) return;
        container.innerHTML = '';
        messages.forEach(m => {
            const div = document.createElement('div');
            div.className = `message ${m.role === 'user' ? 'user' : 'bot'}-message`;
            div.innerHTML = `<p>${renderMarkdownBasic(m.content || '')}</p>`;
            container.appendChild(div);
        });
        container.scrollTop = container.scrollHeight;
    } catch (e) {}
}

// restore on open
(function () {
    document.addEventListener('DOMContentLoaded', restoreChatHistory);
})();

// Add smooth transitions to all interactive elements
document.addEventListener('DOMContentLoaded', () => {
    const interactiveElements = document.querySelectorAll('a, button, input, select, textarea');
    
    interactiveElements.forEach(element => {
        element.style.transition = 'all 0.3s ease';
    });
    
    // Initialize tool buttons if they exist
    initializeToolButtons();
});

// Initialize tool buttons
function initializeToolButtons() {
    // Budget Optimizer button
    const budgetBtn = document.querySelector('[onclick="openBudgetOptimizer()"]');
    if (budgetBtn) {
        budgetBtn.addEventListener('click', openBudgetOptimizer);
    }
    
    // Investment Guide button
    const investmentBtn = document.querySelector('[onclick="openInvestmentGuide()"]');
    if (investmentBtn) {
        investmentBtn.addEventListener('click', openInvestmentGuide);
    }
    
    // Portfolio Optimizer button
    const portfolioBtn = document.querySelector('[onclick="openPortfolioOptimizer()"]');
    if (portfolioBtn) {
        portfolioBtn.addEventListener('click', openPortfolioOptimizer);
    }
}

// Tool opening functions
function openBudgetOptimizer() {
    // You can implement a modal or redirect to budget optimizer page
    showNotification('Opening Budget Optimizer...', 'info');
    // Add your budget optimizer modal/page logic here
}

function openInvestmentGuide() {
    showNotification('Opening Investment Guide...', 'info');
    // Add your investment guide modal/page logic here
}

function openPortfolioOptimizer() {
    showNotification('Opening Portfolio Optimizer...', 'info');
    // Add your portfolio optimizer modal/page logic here
}

// Performance optimization: Lazy load images and defer non-critical scripts
function lazyLoadImages() {
    const images = document.querySelectorAll('img[data-src]');
    
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                imageObserver.unobserve(img);
            }
        });
    });
    
    images.forEach(img => imageObserver.observe(img));
}

// Initialize lazy loading
document.addEventListener('DOMContentLoaded', lazyLoadImages);

// Add keyboard navigation support
document.addEventListener('keydown', (e) => {
    // Tab navigation for forms
    if (e.key === 'Tab') {
        const focusableElements = document.querySelectorAll('a, button, input, select, textarea, [tabindex]:not([tabindex="-1"])');
        const firstElement = focusableElements[0];
        const lastElement = focusableElements[focusableElements.length - 1];
        
        if (e.shiftKey && document.activeElement === firstElement) {
            e.preventDefault();
            lastElement.focus();
        } else if (!e.shiftKey && document.activeElement === lastElement) {
            e.preventDefault();
            firstElement.focus();
        }
    }
    
    // Enter key for buttons
    if (e.key === 'Enter' && document.activeElement.tagName === 'BUTTON') {
        document.activeElement.click();
    }
});

// Add accessibility improvements
document.addEventListener('DOMContentLoaded', () => {
    // Add ARIA labels to interactive elements
    const buttons = document.querySelectorAll('button:not([aria-label])');
    buttons.forEach(button => {
        if (button.textContent.trim()) {
            button.setAttribute('aria-label', button.textContent.trim());
        }
    });
    
    // Add skip to content link
    const skipLink = document.createElement('a');
    skipLink.href = '#main-content';
    skipLink.textContent = 'Skip to main content';
    skipLink.style.cssText = `
        position: absolute;
        top: -40px;
        left: 6px;
        background: #667eea;
        color: white;
        padding: 8px;
        text-decoration: none;
        border-radius: 4px;
        z-index: 10000;
        transition: top 0.3s;
    `;
    
    skipLink.addEventListener('focus', () => {
        skipLink.style.top = '6px';
    });
    
    skipLink.addEventListener('blur', () => {
        skipLink.style.top = '-40px';
    });
    
    document.body.insertBefore(skipLink, document.body.firstChild);
    
    // Add main content landmark
    const mainContent = document.querySelector('main') || document.querySelector('.dashboard-main') || document.querySelector('.tool-main');
    if (mainContent) {
        mainContent.id = 'main-content';
        mainContent.setAttribute('role', 'main');
    }
});

// Dark Mode Toggle
function toggleTheme() {
    const body = document.body;
    const themeIcon = document.getElementById('theme-icon');
    const currentTheme = body.getAttribute('data-theme');
    
    if (currentTheme === 'dark') {
        body.removeAttribute('data-theme');
        themeIcon.className = 'fas fa-moon';
        localStorage.setItem('theme', 'light');
        console.log('Switched to light mode');
    } else {
        body.setAttribute('data-theme', 'dark');
        themeIcon.className = 'fas fa-sun';
        localStorage.setItem('theme', 'dark');
        console.log('Switched to dark mode');
    }
}

// Load saved theme
document.addEventListener('DOMContentLoaded', function() {
    const savedTheme = localStorage.getItem('theme');
    const themeIcon = document.getElementById('theme-icon');
    
    if (savedTheme === 'dark') {
        document.body.setAttribute('data-theme', 'dark');
        if (themeIcon) {
            themeIcon.className = 'fas fa-sun';
        }
        console.log('Loaded dark mode');
    } else {
        document.body.removeAttribute('data-theme');
        if (themeIcon) {
            themeIcon.className = 'fas fa-moon';
        }
        console.log('Loaded light mode');
    }
});

// Statistics Counter Animation
function animateCounters() {
    const counters = document.querySelectorAll('.stat-number');
    
    counters.forEach(counter => {
        const target = parseInt(counter.getAttribute('data-target'));
        const increment = target / 100;
        let current = 0;
        
        const updateCounter = () => {
            if (current < target) {
                current += increment;
                counter.textContent = Math.floor(current).toLocaleString();
                requestAnimationFrame(updateCounter);
            } else {
                counter.textContent = target.toLocaleString();
            }
        };
        
        updateCounter();
    });
}

// Intersection Observer for Statistics
const statsObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            animateCounters();
            statsObserver.unobserve(entry.target);
        }
    });
}, { threshold: 0.5 });

// Observe statistics section
document.addEventListener('DOMContentLoaded', function() {
    const statsSection = document.querySelector('.statistics');
    if (statsSection) {
        statsObserver.observe(statsSection);
    }
});

// Newsletter Form Handling
document.addEventListener('DOMContentLoaded', function() {
    const newsletterForm = document.getElementById('newsletterForm');
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const email = document.getElementById('newsletterEmail').value;
            
            if (!isValidEmail(email)) {
                showNotification('Please enter a valid email address', 'error');
                return;
            }
            
            // Show loading state
            const submitBtn = this.querySelector('button[type="submit"]');
            const originalText = submitBtn.innerHTML;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Subscribing...';
            submitBtn.disabled = true;
            
            // Simulate API call
            setTimeout(() => {
                showNotification('Thank you for subscribing! You\'ll receive our weekly financial tips.', 'success');
                this.reset();
                submitBtn.innerHTML = originalText;
                submitBtn.disabled = false;
            }, 2000);
        });
    }
});

// Loading States
function showLoading() {
    document.getElementById('loadingOverlay').style.display = 'flex';
}

function hideLoading() {
    document.getElementById('loadingOverlay').style.display = 'none';
}

// Progress Bar
function updateProgressBar(percent) {
    const progressFill = document.querySelector('.progress-fill');
    if (progressFill) {
        progressFill.style.width = percent + '%';
    }
}

// Scroll Progress
window.addEventListener('scroll', () => {
    const scrollTop = window.pageYOffset;
    const docHeight = document.body.scrollHeight - window.innerHeight;
    const scrollPercent = (scrollTop / docHeight) * 100;
    updateProgressBar(scrollPercent);
});

// Enhanced Error Handling
window.addEventListener('error', function(e) {
    console.error('JavaScript Error:', e.error);
    showNotification('Something went wrong. Please refresh the page.', 'error');
});

// Offline Support
window.addEventListener('online', function() {
    showNotification('Connection restored!', 'success');
});

window.addEventListener('offline', function() {
    showNotification('You are offline. Some features may not work.', 'warning');
});

// Enhanced Form Validation
function validateForm(form) {
    const inputs = form.querySelectorAll('input[required], textarea[required]');
    let isValid = true;
    
    inputs.forEach(input => {
        if (!input.value.trim()) {
            input.style.borderColor = '#f44336';
            isValid = false;
        } else {
            input.style.borderColor = '#e1e5e9';
        }
    });
    
    return isValid;
}

// Add loading states to all forms
document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!validateForm(this)) {
                e.preventDefault();
                showNotification('Please fill in all required fields', 'error');
                return;
            }
            
            // Add loading state to submit button
            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn && !submitBtn.disabled) {
                const originalText = submitBtn.innerHTML;
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
                submitBtn.disabled = true;
                
                // Reset after 3 seconds (for demo purposes)
                setTimeout(() => {
                    submitBtn.innerHTML = originalText;
                    submitBtn.disabled = false;
                }, 3000);
            }
        });
    });
});

// Enhanced Notification System
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : type === 'warning' ? 'exclamation-triangle' : 'info-circle'}"></i>
            <span class="notification-message">${message}</span>
            <button class="notification-close">&times;</button>
        </div>
    `;
    
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${type === 'success' ? '#4CAF50' : type === 'error' ? '#f44336' : type === 'warning' ? '#ff9800' : '#2196F3'};
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        z-index: 10000;
        transform: translateX(100%);
        transition: transform 0.3s ease;
        max-width: 300px;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
    }, 100);
    
    setTimeout(() => {
        notification.style.transform = 'translateX(100%)';
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 300);
    }, 5000);
    
    const closeBtn = notification.querySelector('.notification-close');
    closeBtn.addEventListener('click', () => {
        notification.style.transform = 'translateX(100%)';
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 300);
    });
}

// Performance Optimization
function lazyLoadImages() {
    const images = document.querySelectorAll('img[data-src]');
    
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                imageObserver.unobserve(img);
            }
        });
    });
    
    images.forEach(img => imageObserver.observe(img));
}

// Navigation scroll effect
window.addEventListener('scroll', function() {
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > 50) {
        navbar.classList.add('scrolled');
    } else {
        navbar.classList.remove('scrolled');
    }
});

// Initialize all enhancements
document.addEventListener('DOMContentLoaded', function() {
    lazyLoadImages();
    
    // Add smooth scroll to all anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Add loading state to external links
    document.querySelectorAll('a[href^="http"]').forEach(link => {
        link.addEventListener('click', function() {
            showLoading();
            setTimeout(hideLoading, 2000);
        });
    });
    
    // Add active class to current page navigation
    const currentPage = window.location.pathname.split('/').pop() || 'index.html';
    document.querySelectorAll('.nav-link').forEach(link => {
        if (link.getAttribute('href') === currentPage) {
            link.classList.add('active');
        }
    });
});

console.log('Ghar Ka Guide website initialized successfully with Python backend integration and enhanced features!');

// =============================
// Lightweight client-side auth
// =============================

function isAuthenticated() {
    return Boolean(localStorage.getItem('authToken'));
}

function redirectToLogin(withRedirectTo) {
    const target = withRedirectTo || window.location.pathname + window.location.search + window.location.hash;
    const encoded = encodeURIComponent(target);
    window.location.href = `login.html?redirect=${encoded}`;
}

function logout() {
    try {
        localStorage.removeItem('authToken');
        localStorage.removeItem('userData');
    } catch (e) {
        console.warn('Failed clearing auth storage', e);
    }
    showNotification('You have been logged out.', 'info');
    setTimeout(() => {
        window.location.href = 'index.html';
    }, 500);
}

// Guard protected pages on load
(function guardProtectedPagesOnLoad() {
    const protectedPages = ['dashboard.html', 'budget-optimizer.html', 'investment-guide.html'];
    const path = (window.location.pathname.split('/').pop() || 'index.html').toLowerCase();
    if (protectedPages.includes(path) && !isAuthenticated()) {
        redirectToLogin(window.location.pathname + window.location.search + window.location.hash);
    }
})();

// Intercept clicks to protected pages site-wide
document.addEventListener('click', function(e) {
    const anchor = e.target.closest('a[href]');
    if (!anchor) return;
    const href = anchor.getAttribute('href');
    if (!href) return;
    const protectedTargets = ['dashboard.html', 'budget-optimizer.html', 'investment-guide.html'];
    const isProtected = protectedTargets.some(name => href.toLowerCase().includes(name));
    if (isProtected && !isAuthenticated()) {
        e.preventDefault();
        redirectToLogin(href);
    }
});

// If we land on login with a redirect param and are already logged in, go there
document.addEventListener('DOMContentLoaded', function() {
    const path = (window.location.pathname.split('/').pop() || '').toLowerCase();
    if (path === 'login.html') {
        const params = new URLSearchParams(window.location.search);
        const redirectParam = params.get('redirect');
        if (isAuthenticated() && redirectParam) {
            window.location.href = decodeURIComponent(redirectParam);
        }
        // Listen for successful login (token presence) and honor redirect param
        const observer = new MutationObserver(() => {
            if (isAuthenticated() && redirectParam) {
                window.location.href = decodeURIComponent(redirectParam);
            }
        });
        observer.observe(document.body, { childList: true, subtree: true });
        // Auto-stop after a short period
        setTimeout(() => observer.disconnect(), 5000);
    }
});

// =============================
// Error Logging & Analytics
// =============================

const ErrorLogger = {
    // Log errors to backend
    async logError(error, context = {}) {
        const errorData = {
            message: error.message || String(error),
            stack: error.stack || '',
            url: window.location.href,
            userAgent: navigator.userAgent,
            timestamp: new Date().toISOString(),
            context: context
        };

        // Try to send to backend
        try {
            await fetch('/api/errors/log', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(errorData)
            });
        } catch (e) {
            // Fallback: log to console if backend unavailable
            console.error('Error logging failed:', e);
            console.error('Original error:', errorData);
        }
    },

    // Track custom events for analytics
    trackEvent(eventName, properties = {}) {
        // Plausible analytics (if available)
        if (window.plausible) {
            window.plausible(eventName, { props: properties });
        }
        
        // Also log to backend for custom analytics
        try {
            fetch('/api/analytics/track', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    event: eventName,
                    properties: properties,
                    timestamp: new Date().toISOString(),
                    url: window.location.href
                })
            }).catch(() => {}); // Silent fail for analytics
        } catch (e) {
            // Silent fail
        }
    }
};

// Global error handlers
window.addEventListener('error', (event) => {
    ErrorLogger.logError(event.error || new Error(event.message), {
        filename: event.filename,
        lineno: event.lineno,
        colno: event.colno,
        type: 'javascript_error'
    });
});

window.addEventListener('unhandledrejection', (event) => {
    ErrorLogger.logError(event.reason || new Error('Unhandled Promise Rejection'), {
        type: 'unhandled_promise_rejection'
    });
});

// Track page views
if (typeof window !== 'undefined') {
    ErrorLogger.trackEvent('page_view', {
        path: window.location.pathname,
        referrer: document.referrer
    });
}

// Track important user actions
document.addEventListener('click', (e) => {
    const target = e.target.closest('a, button, [role="button"]');
    if (target) {
        const text = target.textContent?.trim() || target.getAttribute('aria-label') || '';
        const href = target.getAttribute('href') || '';
        if (text || href) {
            ErrorLogger.trackEvent('click', {
                element: target.tagName.toLowerCase(),
                text: text.substring(0, 50),
                href: href.substring(0, 100)
            });
        }
    }
}, true);

// Track form submissions
document.addEventListener('submit', (e) => {
    const form = e.target;
    if (form.tagName === 'FORM') {
        ErrorLogger.trackEvent('form_submit', {
            formId: form.id || form.name || 'unnamed',
            action: form.action || ''
        });
    }
});
