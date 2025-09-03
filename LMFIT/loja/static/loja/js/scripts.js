  // Configurações do WhatsApp
const WHATSAPP_NUMBER = "5589994077754"; // ⚠️ ALTERE ESTE NÚMERO PARA O SEU WHATSAPP REAL!

// Variáveis globais
let cart = [];
let cartBtn, cartModal, closeCart, cartCount, cartItems, cartTotal, checkoutBtn, mobileMenuBtn, mobileMenu;
let searchInput, categoryFilter, priceFilter, productCards;

// Funções globais para serem acessadas pelo HTML
window.openImageModal = function(imageSrc) {
    console.log('Abrindo modal de imagem:', imageSrc);
    const modal = document.getElementById('image-modal');
    const modalImage = document.getElementById('modal-image');
    
    if (modal && modalImage) {
        modalImage.src = imageSrc;
        modal.classList.remove('hidden');
        document.body.style.overflow = 'hidden';
    } else {
        console.error('Modal ou imagem não encontrados');
    }
};

window.closeImageModal = function() {
    const modal = document.getElementById('image-modal');
    if (modal) {
        modal.classList.add('hidden');
        document.body.style.overflow = 'auto';
    }
};

window.changeMainImage = function(newSrc, mainImageElement) {
    if (mainImageElement) {
        mainImageElement.src = newSrc;
    }
};

// Variáveis para o modal de confirmação
let pendingProduct = null;

window.addToCartWithSize = function(productName, price, sizeSelectId) {
    const sizeSelect = document.getElementById(sizeSelectId);
    if (sizeSelect) {
        const selectedSize = sizeSelect.value;
        
        // Encontrar o card do produto para obter a imagem
        const productCard = sizeSelect.closest('.product-card');
        const productImage = productCard ? productCard.querySelector('.product-main-image') : null;
        
        // Armazenar dados do produto pendente
        pendingProduct = {
            name: productName,
            price: price,
            size: selectedSize,
            image: productImage ? productImage.src : '',
            sizeSelectId: sizeSelectId
        };
        
        // Mostrar modal de confirmação
        showCartConfirmationModal();
    } else {
        console.error('Seletor de tamanho não encontrado:', sizeSelectId);
    }
};

window.buyOnWhatsAppWithSize = function(productName, price, sizeSelectId) {
    const sizeSelect = document.getElementById(sizeSelectId);
    if (sizeSelect) {
        const selectedSize = sizeSelect.value;
        buyOnWhatsApp(productName, price, selectedSize);
    } else {
        console.error('Seletor de tamanho não encontrado:', sizeSelectId);
    }
};

window.filterByCategory = function(category) {
    // Scroll para a seção de produtos
    const produtosSection = document.getElementById('produtos');
    if (produtosSection) {
        produtosSection.scrollIntoView({ behavior: 'smooth' });
    }
    
    // Definir o filtro de categoria
    if (categoryFilter) {
        categoryFilter.value = category;
    }
    
    // Aplicar filtros
    filterProducts();
};

window.updateQuantity = function(index, change) {
    cart = JSON.parse(localStorage.getItem('cart')) || [];
    if (cart[index]) {
        cart[index].quantity += change;
        if (cart[index].quantity <= 0) {
            removeFromCart(index);
        } else {
            localStorage.setItem('cart', JSON.stringify(cart));
            updateCartDisplay();
        }
    }
};

window.removeFromCart = function(index) {
    cart = JSON.parse(localStorage.getItem('cart')) || [];
    if (cart[index]) {
        cart.splice(index, 1);
        localStorage.setItem('cart', JSON.stringify(cart));
        updateCartDisplay();
    }
};

// Funções do carrinho que precisam ser globais
window.addToCart = function(productName, price, size) {
    cart = JSON.parse(localStorage.getItem('cart')) || [];
    const existingItem = cart.find(item => item.name === productName && item.size === size);
    
    if (existingItem) {
        existingItem.quantity += 1;
    } else {
        cart.push({
            name: productName,
            price: price,
            size: size,
            quantity: 1
        });
    }
    
    localStorage.setItem('cart', JSON.stringify(cart));
    updateCartDisplay();
    showCartNotification();
};

window.buyOnWhatsApp = function(productName, price, size) {
    const message = `Olá! Gostei do produto *${productName}*, tamanho *${size}*, valor *R$ ${price.toFixed(2).replace('.', ',')}*. Gostaria de finalizar a compra.`;
    const url = `https://api.whatsapp.com/send?phone=${WHATSAPP_NUMBER}&text=${encodeURIComponent(message)}`;
    window.open(url, '_blank');
};

window.finalizarCompraWhatsApp = function() {
    cart = JSON.parse(localStorage.getItem('cart')) || [];
    if (cart.length === 0) {
        alert('Carrinho vazio!');
        return;
    }
    
    let message = 'Olá! Gostaria de finalizar a compra dos seguintes itens:\n\n';
    let total = 0;
    
    cart.forEach((item, index) => {
        const itemTotal = item.price * item.quantity;
        total += itemTotal;
        message += `${index + 1}. *${item.name}* - Tamanho: *${item.size}* - Quantidade: *${item.quantity}* - R$ ${itemTotal.toFixed(2).replace('.', ',')}\n`;
    });
    
    message += `\n*Total: R$ ${total.toFixed(2).replace('.', ',')}*`;
    
    const url = `https://api.whatsapp.com/send?phone=${WHATSAPP_NUMBER}&text=${encodeURIComponent(message)}`;
    window.open(url, '_blank');
};

window.updateCartDisplay = function() {
    if (!cartCount || !cartTotal || !cartItems) {
        console.log('Elementos do carrinho não encontrados');
        return;
    }
    
    // Atualizar o array cart com os dados do localStorage
    cart = JSON.parse(localStorage.getItem('cart')) || [];
    
    const total = cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
    
    cartCount.textContent = cart.length;
    cartCount.classList.toggle('hidden', cart.length === 0);
    cartTotal.textContent = `R$ ${total.toFixed(2).replace('.', ',')}`;
    
    cartItems.innerHTML = '';
    cart.forEach((item, index) => {
        const itemElement = document.createElement('div');
        itemElement.className = 'flex items-center justify-between p-3 bg-cinza-claro rounded-lg';
        itemElement.innerHTML = `
            <div class="flex-1">
                <h4 class="font-semibold text-preto">${item.name}</h4>
                <p class="text-sm text-cinza-escuro">Tamanho: ${item.size}</p>
                <p class="text-rosa font-bold">R$ ${item.price.toFixed(2).replace('.', ',')}</p>
            </div>
            <div class="flex items-center space-x-2">
                <button onclick="updateQuantity(${index}, -1)" class="bg-rosa text-branco w-8 h-8 rounded-full flex items-center justify-center hover:bg-rosa-escuro">
                    <i class="fas fa-minus text-xs"></i>
                </button>
                <span class="w-8 text-center font-semibold">${item.quantity}</span>
                <button onclick="updateQuantity(${index}, 1)" class="bg-rosa text-branco w-8 h-8 rounded-full flex items-center justify-center hover:bg-rosa-escuro">
                    <i class="fas fa-plus text-xs"></i>
                </button>
                <button onclick="removeFromCart(${index})" class="text-red-500 hover:text-red-700 ml-2">
                    <i class="fas fa-trash"></i>
                </button>
            </div>
        `;
        cartItems.appendChild(itemElement);
    });
};

window.showCartNotification = function() {
    if (cartCount) {
        cartCount.classList.add('cart-badge');
        setTimeout(() => {
            cartCount.classList.remove('cart-badge');
        }, 2000);
    }
    
    // Criar notificação temporária
    const notification = document.createElement('div');
    notification.className = 'fixed top-20 right-4 bg-rosa text-branco px-4 py-2 rounded-lg shadow-lg z-50';
    notification.innerHTML = '<i class="fas fa-check mr-2"></i>Item adicionado ao carrinho!';
    document.body.appendChild(notification);
    
    // Remover notificação após 3 segundos
    setTimeout(() => {
        notification.remove();
    }, 3000);
};

// Funções do modal de confirmação
window.showCartConfirmationModal = function() {
    if (!pendingProduct) return;
    
    const modal = document.getElementById('cart-confirmation-modal');
    const productImage = document.getElementById('confirmation-product-image');
    const productName = document.getElementById('confirmation-product-name');
    const productPrice = document.getElementById('confirmation-product-price');
    const sizeSelect = document.getElementById('confirmation-size-select');
    
    if (modal && productImage && productName && productPrice && sizeSelect) {
        // Preencher informações do produto
        productImage.src = pendingProduct.image;
        productName.textContent = pendingProduct.name;
        productPrice.textContent = `R$ ${pendingProduct.price.toFixed(2).replace('.', ',')}`;
        sizeSelect.value = pendingProduct.size;
        
        // Mostrar modal
        modal.classList.remove('hidden');
        document.body.style.overflow = 'hidden';
    }
};

window.closeCartConfirmationModal = function() {
    const modal = document.getElementById('cart-confirmation-modal');
    if (modal) {
        modal.classList.add('hidden');
        document.body.style.overflow = 'auto';
        pendingProduct = null;
    }
};

window.confirmAddToCart = function() {
    if (!pendingProduct) return;
    
    const sizeSelect = document.getElementById('confirmation-size-select');
    const selectedSize = sizeSelect ? sizeSelect.value : pendingProduct.size;
    
    // Adicionar ao carrinho
    addToCart(pendingProduct.name, pendingProduct.price, selectedSize);
    
    // Fechar modal
    closeCartConfirmationModal();
};

// Aguardar o DOM estar pronto
document.addEventListener('DOMContentLoaded', function() {
  
  // Elementos DOM
  cartBtn = document.getElementById('cart-btn');
  cartModal = document.getElementById('cart-modal');
  closeCart = document.getElementById('close-cart');
  cartCount = document.getElementById('cart-count');
  cartItems = document.getElementById('cart-items');
  cartTotal = document.getElementById('cart-total');
  checkoutBtn = document.getElementById('checkout-whatsapp');
  mobileMenuBtn = document.getElementById('mobile-menu-btn');
  mobileMenu = document.getElementById('mobile-menu');
  
  // Verificar se os elementos foram encontrados
  console.log('Elementos DOM carregados:', {
      cartBtn: !!cartBtn,
      cartModal: !!cartModal,
      closeCart: !!closeCart,
      cartCount: !!cartCount,
      cartItems: !!cartItems,
      cartTotal: !!cartTotal,
      checkoutBtn: !!checkoutBtn,
      mobileMenuBtn: !!mobileMenuBtn,
      mobileMenu: !!mobileMenu
  });
  
  // Funções do carrinho agora são globais (definidas acima)
  

  
  // Função para finalizar carrinho no WhatsApp (redireciona para a nova função)
  function checkoutCart() {
      finalizarCompraWhatsApp();
  }
  
  // Event Listeners
  if (cartBtn && cartModal) {
      cartBtn.addEventListener('click', () => {
          cartModal.classList.remove('hidden');
      });
  }
  
  if (closeCart && cartModal) {
      closeCart.addEventListener('click', () => {
          cartModal.classList.add('hidden');
      });
  }
  
  // Event listener para o botão de finalizar no WhatsApp
  const checkoutWhatsAppBtn = document.getElementById('checkout-whatsapp');
  if (checkoutWhatsAppBtn) {
      checkoutWhatsAppBtn.addEventListener('click', finalizarCompraWhatsApp);
  }
  
  if (checkoutBtn) {
      checkoutBtn.addEventListener('click', checkoutCart);
  }
  
  // Fechar modal clicando fora
  if (cartModal) {
      cartModal.addEventListener('click', (e) => {
          if (e.target === cartModal) {
              cartModal.classList.add('hidden');
          }
      });
  }
  
  // Menu mobile
  if (mobileMenuBtn && mobileMenu) {
      mobileMenuBtn.addEventListener('click', () => {
          mobileMenu.classList.toggle('hidden');
      });
  }
  
  // Smooth scroll para links de navegação
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
      anchor.addEventListener('click', function (e) {
          e.preventDefault();
          const target = document.querySelector(this.getAttribute('href'));
          if (target) {
              target.scrollIntoView({
                  behavior: 'smooth',
                  block: 'start'
              });
              // Fechar menu mobile se estiver aberto
              mobileMenu.classList.add('hidden');
          }
      });
  });
  
  // Scroll suave para o topo
  window.addEventListener('scroll', () => {
      const header = document.querySelector('header');
      if (window.scrollY > 100) {
          header.classList.add('shadow-xl');
      } else {
          header.classList.remove('shadow-xl');
      }
  });
  
  // Inicializar carrinho
  if (cartItems && cartTotal && cartCount) {
      updateCartDisplay();
  }
  
  // Funcionalidades de pesquisa e filtro
  searchInput = document.getElementById('search-input');
  categoryFilter = document.getElementById('category-filter');
  priceFilter = document.getElementById('price-filter');
  productCards = document.querySelectorAll('.product-card');
  
  console.log('Elementos de filtro carregados:', {
      searchInput: !!searchInput,
      categoryFilter: !!categoryFilter,
      priceFilter: !!priceFilter,
      productCards: productCards.length
  });
  
  // Função para filtrar produtos
  function filterProducts() {
      if (!searchInput || !categoryFilter || !priceFilter) {
          console.log('Elementos de filtro não encontrados');
          return;
      }
      
      const searchTerm = searchInput.value.toLowerCase();
      const selectedCategory = categoryFilter.value;
      const selectedPrice = priceFilter.value;
      
      productCards.forEach(card => {
          const productName = card.getAttribute('data-name').toLowerCase();
          const productCategory = card.getAttribute('data-category');
          const productPrice = parseFloat(card.getAttribute('data-price'));
          
          let showCard = true;
          
          // Filtro por pesquisa
          if (searchTerm && !productName.includes(searchTerm)) {
              showCard = false;
          }
          
          // Filtro por categoria
          if (selectedCategory && productCategory !== selectedCategory) {
              showCard = false;
          }
          
          // Filtro por preço
          if (selectedPrice) {
              const [min, max] = selectedPrice.split('-').map(p => p === '+' ? Infinity : parseFloat(p));
              if (productPrice < min || (max !== Infinity && productPrice > max)) {
                  showCard = false;
              }
          }
          
          // Mostrar ou esconder card
          if (showCard) {
              card.style.display = 'block';
          } else {
              card.style.display = 'none';
          }
      });
  }
  
  // Função para filtrar por categoria (chamada pelos cards de categoria)
  function filterByCategory(category) {
      // Scroll para a seção de produtos
      const produtosSection = document.getElementById('produtos');
      if (produtosSection) {
          produtosSection.scrollIntoView({ behavior: 'smooth' });
      }
      
      // Definir o filtro de categoria
      if (categoryFilter) {
          categoryFilter.value = category;
      }
      
      // Aplicar filtros
      filterProducts();
  }
  
  // Event listeners para pesquisa e filtros
  if (searchInput) {
      searchInput.addEventListener('input', filterProducts);
  }
  if (categoryFilter) {
      categoryFilter.addEventListener('change', filterProducts);
  }
  if (priceFilter) {
      priceFilter.addEventListener('change', filterProducts);
  }
  
  // Funções para gerenciar imagens dos produtos
  function changeMainImage(newSrc, mainImageElement) {
      mainImageElement.src = newSrc;
  }
  
  function openImageModal(imageSrc) {
      console.log('Abrindo modal de imagem:', imageSrc);
      const modal = document.getElementById('image-modal');
      const modalImage = document.getElementById('modal-image');
      
      if (modal && modalImage) {
          modalImage.src = imageSrc;
          modal.classList.remove('hidden');
          document.body.style.overflow = 'hidden';
      } else {
          console.error('Modal ou imagem não encontrados');
      }
  }
  
  function closeImageModal() {
      const modal = document.getElementById('image-modal');
      modal.classList.add('hidden');
      document.body.style.overflow = 'auto';
  }
  
  // Fechar modal ao clicar fora da imagem
  const imageModal = document.getElementById('image-modal');
  if (imageModal) {
      imageModal.addEventListener('click', function(e) {
          if (e.target === this) {
              closeImageModal();
          }
      });
  }
  
  // Fechar modal com tecla ESC
  document.addEventListener('keydown', function(e) {
      if (e.key === 'Escape') {
          closeImageModal();
          closeCartConfirmationModal();
      }
  });
  
  // Fechar modal de confirmação ao clicar fora
  const cartConfirmationModal = document.getElementById('cart-confirmation-modal');
  if (cartConfirmationModal) {
      cartConfirmationModal.addEventListener('click', function(e) {
          if (e.target === this) {
              closeCartConfirmationModal();
          }
      });
  }
  
  // Funções do carrinho agora são globais (definidas acima)

}); // Fechar DOMContentLoaded