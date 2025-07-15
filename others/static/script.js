// Initialize script
(function() {
    // No need for dark mode initialization as it's now the default
})();

document.addEventListener('DOMContentLoaded', function() {
    // Elements
    const bookContainer = document.getElementById('bookContainer');
    const modal = document.getElementById('bookModal');
    const modalContent = document.getElementById('modalContent');
    const bookSidebar = document.querySelector('.book-sidebar');
    const closeButton = document.querySelector('.close-button');
      // Helper function to get the most recent image timestamp for a book folder
    function getLatestImageTimestamp(folder) {
        // Since we can't directly access the filesystem from the browser,
        // we'll use a simple pattern based on folder structure with the actual timestamps
        
        // For known folders, return the exact timestamps based on actual files
        const folderTimestampMap = {
            'book_about_space_exploration_in_the_distant_future': '20250412_212549',
            'book_about_an_indian_crime_thriller': '20250412_214949',
            'book_about_i_love_you_maya': '20250504_102135',
            'book_about_my_incomple_love_story_from_10th_grade': '20250503_222720',
            'book_about_lost_in_your_memories_forever': '20250511_000153',
            'book_about_dark_romance': '20250511_144312'
        };
        
        // Return known timestamp or generate a reasonable one
        return folderTimestampMap[folder] || '20250501_000000';
    }
    const searchInput = document.getElementById('searchInput');
    const filterButtons = document.querySelectorAll('.filter-btn');
    const gridViewBtn = document.getElementById('gridView');
    const listViewBtn = document.getElementById('listView');
    const prevChapterBtn = document.getElementById('prevChapter');
    const nextChapterBtn = document.getElementById('nextChapter');
    const bookInfoBtn = document.getElementById('bookInfo');    const fontSizeBtn = document.getElementById('fontSizeBtn');
    const bookmarkBtn = document.getElementById('bookmarkBtn');
    
    let currentChapterIndex = 0;
    let currentBookDetails = null;
    let fontSizeIndex = parseInt(localStorage.getItem('fontSizeIndex') || '1'); // 0: small, 1: medium, 2: large
    let bookmarks = JSON.parse(localStorage.getItem('bookmarks') || '{}');
    
    // View mode buttons
    gridViewBtn.addEventListener('click', function() {
        if (!this.classList.contains('active')) {
            listViewBtn.classList.remove('active');
            this.classList.add('active');
            bookContainer.classList.remove('list-view');
        }
    });
    
    listViewBtn.addEventListener('click', function() {
        if (!this.classList.contains('active')) {
            gridViewBtn.classList.remove('active');
            this.classList.add('active');
            bookContainer.classList.add('list-view');
        }
    });
    
    // Filter buttons
    filterButtons.forEach(button => {
        button.addEventListener('click', function() {
            filterButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
            const filter = this.getAttribute('data-filter');
            filterBooks(filter);
        });
    });
    
    // Search functionality
    searchInput.addEventListener('input', debounce(function() {
        const query = this.value.toLowerCase().trim();
        searchBooks(query);
    }, 300));
    
    // Font size toggle
    fontSizeBtn.addEventListener('click', function() {
        fontSizeIndex = (fontSizeIndex + 1) % 3;
        const bookMain = document.querySelector('.book-main');
        
        if (bookMain) {
            bookMain.classList.remove('font-small', 'font-medium', 'font-large');
            
            switch(fontSizeIndex) {
                case 0:
                    bookMain.classList.add('font-small');
                    break;
                case 1:
                    bookMain.classList.add('font-medium');
                    break;
                case 2:
                    bookMain.classList.add('font-large');
                    break;
            }
            
            // Store the font size preference
            localStorage.setItem('fontSizeIndex', fontSizeIndex);
        }
    });
      // Bookmark functionality
    bookmarkBtn.addEventListener('click', function() {
        if (!currentBookDetails) return;
        
        const bookId = currentBookDetails.id;
        if (!bookmarks[bookId]) {
            bookmarks[bookId] = [];
        }
        
        // Check if current chapter is already bookmarked
        const chapterIndex = bookmarks[bookId].indexOf(currentChapterIndex);
        
        if (chapterIndex === -1) {
            // Add bookmark
            bookmarks[bookId].push(currentChapterIndex);
            this.querySelector('i').classList.add('active');
        } else {
            // Remove bookmark
            bookmarks[bookId].splice(chapterIndex, 1);
            this.querySelector('i').classList.remove('active');
        }
        
        // Store bookmarks
        localStorage.setItem('bookmarks', JSON.stringify(bookmarks));
    });
    
    // Apply saved font size on page load
    const savedFontSize = localStorage.getItem('fontSizeIndex');
    if (savedFontSize !== null) {
        fontSizeIndex = parseInt(savedFontSize);
        // We'll apply this when a book is opened
    }
    
    // Navigation controls
    prevChapterBtn.addEventListener('click', function() {
        if (currentChapterIndex > 0) {
            currentChapterIndex--;
            displayChapter(currentBookDetails.chapters[currentChapterIndex]);
            updateChapterNav();
        }
    });
    
    nextChapterBtn.addEventListener('click', function() {
        if (currentChapterIndex < currentBookDetails.chapters.length - 1) {
            currentChapterIndex++;
            displayChapter(currentBookDetails.chapters[currentChapterIndex]);
            updateChapterNav();
        }
    });
    
    bookInfoBtn.addEventListener('click', function() {
        if (currentBookDetails) {
            showBookOverview(currentBookDetails);
        }
    });
    
    // Close modal with button and when clicking outside
    closeButton.addEventListener('click', function() {
        closeModal();
    });
    
    window.addEventListener('click', function(event) {
        if (event.target === modal) {
            closeModal();
        }
    });
    
    // Keyboard navigation
    document.addEventListener('keydown', function(e) {
        if (modal.style.display === 'block') {
            if (e.key === 'Escape') {
                closeModal();
            } else if (e.key === 'ArrowLeft') {
                if (currentChapterIndex > 0) {
                    currentChapterIndex--;
                    displayChapter(currentBookDetails.chapters[currentChapterIndex]);
                    updateChapterNav();
                }
            } else if (e.key === 'ArrowRight') {
                if (currentChapterIndex < currentBookDetails.chapters.length - 1) {
                    currentChapterIndex++;
                    displayChapter(currentBookDetails.chapters[currentChapterIndex]);
                    updateChapterNav();
                }
            }
        }
    });
    
    function closeModal() {
        modal.classList.remove('show');
        setTimeout(() => {
            modal.style.display = 'none';
            document.body.style.overflow = '';
        }, 300);
    }
    
    // Fetch and display all books
    fetchBooks();
    
    async function fetchBooks() {
        try {
            // Fetch the books directory structure
            const response = await fetch('/books-structure');
            
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            
            const books = await response.json();
            displayBooks(books);
            
        } catch (error) {
            console.error('Error fetching books:', error);
            // Since this is a static site with no backend, let's provide sample data
            fetchStaticBooks();
        }
    }
      // For static sites without a server, we can build the structure manually
    function fetchStaticBooks() {
        // Get directories under the books folder
        const bookFolders = [
            'book_about_space_exploration_in_the_distant_future',
            'book_about_an_indian_crime_thriller',
            'book_about_i_love_you_maya',
            'book_about_my_incomple_love_story_from_10th_grade',
            'book_about_lost_in_your_memories_forever',
            'book_about_dark_romance'
        ];
        
        const books = [];
        
        // Create promises for each book
        const bookPromises = bookFolders.map(folder => {
            return fetch(`books/${folder}/book_metadata.json`)
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`Failed to fetch metadata for ${folder}`);
                    }
                    return response.json();
                })                .then(metadata => {                    // Get the first chapter illustration as cover image
                    const firstChapterNum = '01';
                    // Construct a specific path pattern based on the folder structure
                    // We'll use the pattern that matches our file system: chapter_01_chapter_1_20250412_214949.png
                    const coverImagePath = `books/${folder}/illustrations/chapter_${firstChapterNum}_chapter_1_`;
                    
                    return {
                        id: folder,
                        title: metadata.book_info.title,
                        description: metadata.book_info.description,
                        date: metadata.book_info.creation_date,
                        chapters: metadata.book_info.total_chapters,
                        folder: folder,
                        coverImagePath: coverImagePath
                    };
                })
                .catch(error => {
                    console.error(`Error fetching ${folder}:`, error);
                    // Return basic info from the folder name
                    return {
                        id: folder,
                        title: folder.replace(/_/g, ' ').replace('book_about_', ''),
                        description: 'A generated story',
                        date: 'Unknown',
                        chapters: 'Unknown',
                        folder: folder
                    };
                });
        });
        
        // Wait for all promises to resolve
        Promise.all(bookPromises)
            .then(booksData => {
                displayBooks(booksData);
            })
            .catch(error => {
                console.error('Error fetching books data:', error);
                displayErrorMessage();
            });
    }
    
    function displayBooks(books) {
        // Clear loading message
        bookContainer.innerHTML = '';
        
        if (books.length === 0) {
            bookContainer.innerHTML = '<div class="no-books">No books found.</div>';
            return;
        }
        
        // Display each book
        books.forEach(book => {
            const bookCard = createBookCard(book);
            bookContainer.appendChild(bookCard);
        });
    }
      // Helper function for debouncing
    function debounce(func, wait) {
        let timeout;
        return function() {
            const context = this;
            const args = arguments;
            clearTimeout(timeout);
            timeout = setTimeout(() => {
                func.apply(context, args);
            }, wait);
        };
    }
    
    // Search books
    function searchBooks(query) {
        const bookCards = document.querySelectorAll('.book-card');
        if (query === '') {
            // Show all books
            bookCards.forEach(card => {
                card.style.display = '';
                card.classList.add('slide-up');
            });
        } else {
            bookCards.forEach(card => {
                const title = card.querySelector('h2').textContent.toLowerCase();
                const description = card.querySelector('.book-info p').textContent.toLowerCase();
                
                if (title.includes(query) || description.includes(query)) {
                    card.style.display = '';
                    card.classList.add('slide-up');
                } else {
                    card.style.display = 'none';
                    card.classList.remove('slide-up');
                }
            });
        }
    }
    
    // Filter books by category
    function filterBooks(category) {
        const bookCards = document.querySelectorAll('.book-card');
        if (category === 'all') {
            bookCards.forEach(card => {
                card.style.display = '';
                card.classList.add('slide-up');
            });
        } else {
            bookCards.forEach(card => {
                // In a real scenario, books would have category metadata
                // For now, we'll do some basic matching based on title/description
                const title = card.querySelector('h2').textContent.toLowerCase();
                const description = card.querySelector('.book-info p').textContent.toLowerCase();
                
                if (title.includes(category) || description.includes(category)) {
                    card.style.display = '';
                    card.classList.add('slide-up');
                } else {
                    card.style.display = 'none';
                    card.classList.remove('slide-up');
                }
            });
        }
    }

    function createBookCard(book) {
        const bookCard = document.createElement('div');
        bookCard.className = 'book-card slide-up';
        bookCard.setAttribute('data-book-id', book.id || book.folder);
        
        const description = book.description || 'No description available.';
        const shortDesc = description.length > 120 ? description.substring(0, 117) + '...' : description;
        
        // Get a category based on title or description (simplified for demo)
        let category;
        const titleLower = book.title.toLowerCase();
        if (titleLower.includes('space') || titleLower.includes('future')) {
            category = 'sci-fi';
        } else if (titleLower.includes('love') || titleLower.includes('romance')) {
            category = 'romance';
        } else if (titleLower.includes('crime') || titleLower.includes('thriller')) {
            category = 'crime';
        } else {
            category = 'fiction';
        }
        
        bookCard.setAttribute('data-category', category);        // Try to find the first chapter illustration file
        let imgHtml = '';
        if (book.coverImagePath) {
            // We need to handle the specific image names from our file system
            const timestamp = getLatestImageTimestamp(book.folder);
            
            // Log the image path for debugging
            console.log(`Trying to load image: ${book.coverImagePath}${timestamp}.png`);
            
            // Create image element with fallback to text if image fails to load
            imgHtml = `
                <img src="${book.coverImagePath}${timestamp}.png" 
                     alt="${book.title}" 
                     style="width: 100%; height: 100%; object-fit: cover;"
                     onerror="this.style.display='none'; this.nextElementSibling.style.display='flex'; console.log('Image failed to load');" />
                <div class="book-cover" style="display:none;">
                    ${book.title}
                </div>
            `;
        } else {
            imgHtml = `<div class="book-cover">${book.title}</div>`;
        }

        bookCard.innerHTML = `
            <div class="book-image">
                ${imgHtml}
            </div>
            <div class="book-info">
                <h2>${book.title}</h2>
                <p>${shortDesc}</p>
                <div class="book-meta">
                    <span class="date">
                        <i class="fas fa-calendar-alt"></i> 
                        ${book.date || 'Unknown date'}
                    </span>
                    <span class="chapters">
                        <i class="fas fa-book"></i>
                        ${book.chapters || '?'} chapters
                    </span>
                </div>
            </div>
        `;
        
        // Add event listener to open book details
        bookCard.addEventListener('click', function() {
            openBookDetails(book);
        });
        
        return bookCard;
    }
    
    function openBookDetails(book) {
        // Reset reader state
        currentChapterIndex = 0;
        
        // Display loading state
        modalContent.innerHTML = '<div class="loading"><div class="spinner"></div><p class="loading-text">Loading book content...</p></div>';
        document.querySelector('.book-sidebar').innerHTML = '';
        
        // Show the modal with animation
        modal.style.display = 'block';
        document.body.style.overflow = 'hidden'; // Prevent scrolling
        
        // Trigger reflow for animation
        modal.offsetHeight;
        modal.classList.add('show');
        
        // Fetch book metadata and chapters
        fetchBookDetails(book)
            .then(details => {
                currentBookDetails = details;
                displayBookDetails(details);
            })
            .catch(error => {
                console.error('Error fetching book details:', error);
                modalContent.innerHTML = `
                    <div class="book-header">
                        <h2>${book.title}</h2>
                        <p class="error-message">Failed to load book details. Please try again later.</p>
                    </div>
                `;
            });
    }
      async function fetchBookDetails(book) {
        try {
            // Fetch the book metadata
            const response = await fetch(`books/${book.folder}/book_metadata.json`);
            
            if (!response.ok) {
                throw new Error('Failed to fetch book metadata');
            }
            
            const metadata = await response.json();
            
            // Get all chapter files
            const chapterPromises = [];
            const totalChapters = metadata.book_info.total_chapters;
            
            for (let i = 1; i <= totalChapters; i++) {
                const chapterNum = i.toString().padStart(2, '0');
                const chapterFile = `books/${book.folder}/chapter_${chapterNum}_chapter_${i}.md`;
                
                chapterPromises.push(
                    fetch(chapterFile)
                        .then(response => {
                            if (!response.ok) {
                                throw new Error(`Failed to fetch chapter ${i}`);
                            }
                            return response.text();
                        })                        .then(text => {
                            // Extract title from markdown
                            const titleMatch = text.match(/# (.*)/);
                            const title = titleMatch ? titleMatch[1] : `Chapter ${i}`;
                              // Find illustration path if it exists in the markdown
                            let illustrationPath = null;
                            const illustrationMatch = text.match(/!\[.*?\]\((.*?)\)/);
                            if (illustrationMatch) {
                                // Get the relative path from markdown and make it absolute
                                const relativePath = illustrationMatch[1];
                                // Construct the proper path to the illustration
                                illustrationPath = `books/${book.folder}/${relativePath}`;
                                console.log('Illustration path:', illustrationPath);
                            }
                            
                            return {
                                number: i,
                                title: title,
                                content: text,
                                illustrationPath: illustrationPath
                            };
                        })
                        .catch(error => {
                            console.error(`Error fetching chapter ${i}:`, error);
                            return {
                                number: i,
                                title: `Chapter ${i}`,
                                content: 'This chapter could not be loaded.',
                                illustrationPath: null
                            };
                        })
                );
            }
            
            const chapters = await Promise.all(chapterPromises);
            
            return {
                metadata: metadata,
                chapters: chapters,
                folder: book.folder
            };
            
        } catch (error) {
            console.error('Error in fetchBookDetails:', error);
            throw error;
        }
    }
      function displayBookDetails(details) {
        const { metadata, chapters, folder } = details;
        
        // Reset sidebar and fill with chapters
        populateSidebar(metadata, chapters);
        
        // Show book overview first
        showBookOverview(details);
        
        // Apply current font size setting to the book content
        const bookMain = document.querySelector('.book-main');
        if (bookMain) {
            bookMain.classList.remove('font-small', 'font-medium', 'font-large');
            switch(fontSizeIndex) {
                case 0:
                    bookMain.classList.add('font-small');
                    break;
                case 1:
                    bookMain.classList.add('font-medium');
                    break;
                case 2:
                    bookMain.classList.add('font-large');
                    break;
            }
        }
        
        // Update navigation button states
        updateChapterNav();
    }
    
    function populateSidebar(metadata, chapters) {
        // Calculate progress
        const totalChapters = chapters.length;
        const completedChapters = metadata.book_info.completed_chapters || totalChapters;
        const progressPercent = Math.round((completedChapters / totalChapters) * 100);
        
        // Create sidebar content
        let sidebarContent = `
            <div style="padding: 0 1.5rem;">
                <h3 style="font-size: 1.2rem; margin-bottom: 1rem; font-family: 'Playfair Display', serif;">${metadata.book_info.title}</h3>
                
                <div class="book-progress">
                    <div class="progress-bar">
                        <div class="fill" style="width: ${progressPercent}%"></div>
                    </div>
                    <div class="progress-text">${completedChapters} of ${totalChapters} chapters</div>
                </div>
            </div>
            
            <div style="margin-top: 1.5rem;">
                <h4 style="padding: 0 1.5rem; font-size: 0.9rem; font-weight: 500; color: var(--text-tertiary); margin-bottom: 1rem;">CHAPTERS</h4>
                <ul class="chapter-list">
        `;
        
        chapters.forEach(chapter => {
            const chapterTitle = chapter.title.replace(`Chapter ${chapter.number}: `, '');
            
            sidebarContent += `
                <li class="chapter-item" data-chapter="${chapter.number - 1}">
                    <div class="chapter-title">
                        <span class="chapter-num">Chapter ${chapter.number}</span>
                        <span class="chapter-name">${chapterTitle}</span>
                    </div>
                    <div class="chapter-indicator"></div>
                </li>
            `;
        });
        
        sidebarContent += `
                </ul>
            </div>
        `;
        
        // Update the sidebar
        document.querySelector('.book-sidebar').innerHTML = sidebarContent;
        
        // Add event listeners to chapter items
        document.querySelectorAll('.chapter-item').forEach(item => {
            item.addEventListener('click', function() {
                const chapterIndex = parseInt(this.getAttribute('data-chapter'));
                currentChapterIndex = chapterIndex;
                displayChapter(chapters[chapterIndex]);
                updateChapterNav();
            });
        });
    }
    
    function showBookOverview(details) {
        const { metadata, chapters } = details;
        
        // Create book header
        const bookHeader = `
            <div class="book-header">
                <h2>${metadata.book_info.title}</h2>
                <p>${metadata.book_info.description}</p>
                <div class="book-meta">
                    <span><i class="fas fa-calendar-alt"></i> Created: ${metadata.book_info.creation_date}</span>
                    <span><i class="fas fa-book"></i> ${metadata.book_info.total_chapters} chapters</span>
                    <span><i class="fas fa-info-circle"></i> Status: ${metadata.book_info.status}</span>
                </div>
            </div>
            
            <div class="book-details">
                <div class="book-stats">
                    <div class="stat-item">
                        <span class="stat-value">${metadata.book_info.estimated_word_count || 'Unknown'}</span>
                        <span class="stat-label">Words</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-value">${metadata.book_info.estimated_page_count || 'Unknown'}</span>
                        <span class="stat-label">Pages</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-value">${metadata.book_info.topic || 'Fiction'}</span>
                        <span class="stat-label">Category</span>
                    </div>
                </div>
                
                <div class="book-summary">
                    <h3>About This Book</h3>
                    <p>${metadata.book_info.description}</p>
                    <p>This book was generated using AI on ${metadata.book_info.creation_date}.</p>
                    
                    <div class="cta-button" id="startReadingBtn">
                        <i class="fas fa-book-reader"></i> Start Reading
                    </div>
                </div>
            </div>
        `;
        
        // Update the content area
        modalContent.innerHTML = bookHeader;
        
        // Add event listener for the start reading button
        document.getElementById('startReadingBtn').addEventListener('click', function() {
            displayChapter(chapters[0]);
            currentChapterIndex = 0;
            updateChapterNav();
        });
    }    function displayChapter(chapter) {
        // Convert markdown to HTML
        let htmlContent = convertMarkdownToHTML(chapter.content);
          // Check if this chapter has an illustration and add it to HTML
        let illustrationHtml = '';
          if (chapter.illustrationPath) {
            console.log('Displaying illustration:', chapter.illustrationPath);
            illustrationHtml = `
                <div class="chapter-illustration">
                    <img src="${chapter.illustrationPath}" 
                         alt="Chapter ${chapter.number} Illustration" 
                         class="chapter-image" 
                         loading="lazy"
                         onerror="this.onerror=null; console.error('Failed to load image:', this.src); this.src=''; this.parentNode.style.display='none';">
                </div>
            `;
        }
        
        // Set the content
        modalContent.innerHTML = `
            <div class="chapter-content fade-in">
                ${illustrationHtml}
                ${htmlContent}
            </div>
        `;
        
        // Highlight the selected chapter in sidebar
        document.querySelectorAll('.chapter-item').forEach(item => {
            item.classList.remove('active');
            if (parseInt(item.getAttribute('data-chapter')) === currentChapterIndex) {
                item.classList.add('active');
                // Scroll the sidebar to make the active chapter visible
                item.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
        });
        
        // Update bookmark button state
        updateBookmarkState();
        
        // Scroll to the top of the chapter content
        document.querySelector('.book-main').scrollTop = 0;
    }
    
    function updateChapterNav() {
        // Update previous button
        if (currentChapterIndex === 0) {
            prevChapterBtn.classList.add('disabled');
        } else {
            prevChapterBtn.classList.remove('disabled');
        }
        
        // Update next button
        if (!currentBookDetails || currentChapterIndex === currentBookDetails.chapters.length - 1) {
            nextChapterBtn.classList.add('disabled');
        } else {
            nextChapterBtn.classList.remove('disabled');
        }
    }      function convertMarkdownToHTML(markdown) {
        // This is a simple markdown converter, for a real application you might want to use a library
        
        // First, let's remove the illustration image tag (first image in the markdown)
        // since we're handling it separately in displayChapter
        let processedMarkdown = markdown;
        const firstImageMatch = processedMarkdown.match(/!\[.*?\]\(.*?\)/);
        if (firstImageMatch) {
            processedMarkdown = processedMarkdown.replace(firstImageMatch[0], '');
        }
        
        // Handle headers (# Header -> <h1>Header</h1>)
        let html = processedMarkdown
            .replace(/^# (.*?)$/gm, '<h1>$1</h1>')
            .replace(/^## (.*?)$/gm, '<h2>$1</h2>')
            .replace(/^### (.*?)$/gm, '<h3>$1</h3>')
            .replace(/^#### (.*?)$/gm, '<h4>$1</h4>');
          // Handle remaining images ![alt](src) -> <img src="src" alt="alt" class="chapter-image">
        html = html.replace(/!\[(.*?)\]\((.*?)\)/g, function(match, alt, src) {
            // Construct proper path to illustrations if they're relative
            let imagePath = src;
            if (currentBookDetails && src.startsWith('illustrations/')) {
                imagePath = `books/${currentBookDetails.folder}/${src}`;
            }
            return `<img src="${imagePath}" alt="${alt}" class="chapter-image" onerror="this.onerror=null; this.style.display='none';">`;
        });
        
        // Handle bold **text** -> <strong>text</strong>
        html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        
        // Handle italic *text* -> <em>text</em>
        html = html.replace(/\*(.*?)\*/g, '<em>$1</em>');
        
        // Handle paragraphs (lines with a blank line between them)
        html = html.replace(/\n\n/g, '</p><p>');
        
        // Wrap with paragraphs
        html = '<p>' + html + '</p>';
        
        // Clean up any empty paragraphs
        html = html.replace(/<p><\/p>/g, '');
        
        return html;
    }
    
    function displayErrorMessage() {
        bookContainer.innerHTML = `
            <div class="error-message">
                <i class="fas fa-exclamation-circle" style="font-size: 2rem; margin-bottom: 1rem;"></i>
                <h3>Unable to load books</h3>
                <p>There was a problem loading the book collection. Please try again later.</p>
                <button class="retry-btn" onClick="location.reload()">
                    <i class="fas fa-redo"></i> Retry
                </button>
            </div>
        `;
    }
      // Add these additional styles dynamically
    const additionalStyles = document.createElement('style');
    additionalStyles.textContent = `
        .chapter-image {
            max-width: 100%;
            height: auto;
            display: block;
            margin: 2rem auto;
            border-radius: 8px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        .chapter-image:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 20px rgba(0,0,0,0.15);
        }
          .book-stats {
            display: flex;
            justify-content: center;
            gap: 2rem;
            margin: 2rem 0;
            padding: 1.5rem;
            background: rgba(3, 52, 110, 0.5);
            border-radius: var(--border-radius-md);
        }
        
        .stat-item {
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        
        .stat-value {
            font-size: 1.8rem;
            font-weight: 600;
            color: var(--primary-color);
            margin-bottom: 0.5rem;
        }
        
        .stat-label {
            font-size: 0.9rem;
            color: var(--text-tertiary);
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .book-summary {
            margin-top: 2rem;
        }
        
        .book-summary h3 {
            font-family: 'Playfair Display', serif;
            font-size: 1.5rem;
            margin-bottom: 1rem;
            color: var(--text-primary);
        }
        
        .book-summary p {
            margin-bottom: 1rem;
            line-height: 1.7;
        }
          .cta-button {
            display: inline-flex;
            align-items: center;
            gap: 0.8rem;
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            color: var(--accent-color);
            padding: 0.8rem 2rem;
            border-radius: 30px;
            font-weight: 500;
            margin-top: 1.5rem;
            cursor: pointer;
            box-shadow: var(--shadow-md);
            transition: var(--transition-default);
        }
        
        .cta-button:hover {
            transform: translateY(-3px);
            box-shadow: var(--shadow-lg);
        }
        
        .chapter-image {
            max-width: 100%;
            border-radius: var(--border-radius-md);
            box-shadow: var(--shadow-md);
            margin: 2rem auto;
            display: block;
        }
        
        .retry-btn {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            background-color: var(--primary-color);
            color: white;
            border: none;
            padding: 0.7rem 1.5rem;
            border-radius: var(--border-radius-sm);
            cursor: pointer;
            margin-top: 1.5rem;
            transition: var(--transition-default);
        }
        
        .retry-btn:hover {
            background-color: var(--secondary-color);
        }
        
        .control-btn.disabled {
            opacity: 0.4;
            cursor: not-allowed;
        }
        
        /* Font size classes */
        .font-small {
            font-size: 0.9rem;
        }
        
        .font-medium {
            font-size: 1.1rem;
        }
        
        .font-large {
            font-size: 1.3rem;
        }          /* Dark mode is now the default */
            color: #f0f0f0;
        }
        
        html.dark-mode .book-info p { /* Changed from body.dark-mode */
            color: #b0b0b0;
        }
        
        html.dark-mode .book-meta { /* Changed from body.dark-mode */
            border-top-color: #333;
        }
        
        html.dark-mode .book-meta .date,
        html.dark-mode .book-meta .chapters { /* Changed from body.dark-mode */
            color: #999;
        }
        
        html.dark-mode .book-meta .chapters { /* Changed from body.dark-mode */
            background: #2d2d2d;
        }
        
        html.dark-mode .modal-content { /* Changed from body.dark-mode */
            background-color: #1e1e1e;
        }
        
        html.dark-mode .book-sidebar { /* Changed from body.dark-mode */
            background-color: #181818;
            border-right-color: rgba(255, 255, 255, 0.05);
        }
        
        html.dark-mode .chapter-item:hover { /* Changed from body.dark-mode */
            background-color: rgba(255, 255, 255, 0.05);
        }
        
        html.dark-mode .chapter-item.active { /* Changed from body.dark-mode */
            background-color: rgba(67, 97, 238, 0.2);
        }
        
        html.dark-mode .chapter-name { /* Changed from body.dark-mode */
            color: #e0e0e0;
        }
        
        html.dark-mode .close-button,
        html.dark-mode .reader-setting-btn { /* Changed from body.dark-mode */
            background-color: rgba(40, 40, 40, 0.9);
            color: #e0e0e0;
        }
        
        html.dark-mode .book-controls { /* Changed from body.dark-mode */
            background-color: rgba(40, 40, 40, 0.9);
        }
        
        html.dark-mode .control-btn { /* Changed from body.dark-mode */
            color: #b0b0b0;
        }
        html.dark-mode .book-stats { /* Changed from body.dark-mode */
            background: rgba(40, 40, 40, 0.7);
        }
        
        html.dark-mode .chapter-content { /* Changed from body.dark-mode */
            color: #e0e0e0;
        }
        
        html.dark-mode .chapter-content h1, 
        html.dark-mode .chapter-content h2, 
        html.dark-mode .chapter-content h3 { /* Changed from body.dark-mode */
            color: #f0f0f0;
        }
        
        html.dark-mode .chapter-image { /* Changed from body.dark-mode */
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.5);
        }
        
        html.dark-mode footer { /* Changed from body.dark-mode */
            background-color: #181818;
            color: #b0b0b0;
        }
        
        html.dark-mode footer::before { /* Changed from body.dark-mode */
            background: linear-gradient(to bottom, rgba(18, 18, 18, 0), #181818);
        }
        
        html.dark-mode .footer-section h4 { /* Changed from body.dark-mode */
            color: #e0e0e0;
        }
        
        html.dark-mode .footer-section a { /* Changed from body.dark-mode */
            color: #b0b0b0;
        }
        
        html.dark-mode .footer-section a:hover { /* Changed from body.dark-mode */
            color: var(--primary-light);
        }
        
        html.dark-mode .footer-bottom { /* Changed from body.dark-mode */
            border-top-color: #333;
        }
        
        html.dark-mode .cta-button { /* Changed from body.dark-mode */
            background: linear-gradient(135deg, #3a0ca3, #4361ee);
        }
    `;
    document.head.appendChild(additionalStyles);
});

// Function to update bookmark button state
function updateBookmarkState() {
    if (!currentBookDetails) return;
    
    const bookId = currentBookDetails.id;
    const bookmarkIcon = bookmarkBtn.querySelector('i');
    
    if (bookmarks[bookId] && bookmarks[bookId].includes(currentChapterIndex)) {
        bookmarkIcon.classList.add('active');
    } else {
        bookmarkIcon.classList.remove('active');
    }
}