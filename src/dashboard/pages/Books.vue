<template>
  <div>
    <nav-bar></nav-bar>
    <Container>
      <div>
        <b-card title="Books">
          <b-form-input v-model="searchText" placeholder="Search books" @input="filterBooks"></b-form-input>
          <b-button @click="showAddBookModal" variant="success" class="my-3">Add Book</b-button>
          <!-- <b-table striped hover :items="filteredBooks" :fields="tableFields" :current-page="currentPage" :per-page="perPage"> -->
          <b-table
            striped
            hover
            :items="sortedFilteredBooks" 
            :fields="tableFields"
            :current-page="currentPage"
            :per-page="perPage"
            :sort-by.sync="sortBy"
            :sort-desc.sync="sortDesc"
          >

            <template #cell(actions)="row">
              <b-button @click="editBook(row.item)" variant="primary" size="sm">Edit</b-button>
            </template>
          </b-table>
          <b-pagination v-model="currentPage" :total-rows="filteredBooks.length" :per-page="perPage" class="mt-3"></b-pagination>
        </b-card>

        <!-- Add/Edit Book Modal -->
        <b-modal hide-footer v-model="showBookModal" title="Book Details">
          <b-form @submit.prevent="saveBook">
            <b-form-group label="Title">
              <b-form-input v-model="bookForm.title" required></b-form-input>
            </b-form-group>
            <b-form-group label="Author">
              <vue-tree-select
                :options="authorOptions"
                v-model="bookForm.author_id"
                placeholder="Select Author"
                :multiple="false"
                :searchable="true"
                required
              ></vue-tree-select>
            </b-form-group>
            <b-form-group label="Number of Pages">
              <b-form-input v-model="bookForm.pages" type="number" required></b-form-input>
            </b-form-group>
            <b-button type="submit" variant="primary">Save</b-button>
            <b-button @click="hideBookModal" variant="secondary">Cancel</b-button>
          </b-form>
        </b-modal>
      </div>
    </Container>
  </div>
</template>

<script lang="ts">
import { Vue, Component } from 'nuxt-property-decorator';
import {getAccessToken} from "../utils/localStorageHelper";
import VueTreeSelect from '@riophae/vue-treeselect';
import '@riophae/vue-treeselect/dist/vue-treeselect.css'

@Component({
    components: {
    VueTreeSelect,
  },
})
export default class Books extends Vue {
  private searchText: string = '';
  private books: any[] = [];
  private filteredBooks: any[] = [];
  private currentPage: number = 1;
  private perPage: number = 7;
  private accessToken: string = ''
  private sortBy: string = 'title'; // The initial column to sort by
  private sortDesc: boolean = true; // true for descending order, false for ascending order

  private tableFields: any[] = [
    { key: 'title', label: 'Title', sortable: true },
    { key: 'author.name', label: 'Author', sortable: true },
    { key: 'pages', label: 'Number of Pages', sortable: true },
    { key: 'actions', label: 'Actions' },
  ];

  private showBookModal: boolean = false;
  private bookForm: any = {
    title: '',
    author_id: null,
    pages: 0,
  };

  private authors: any[] = [];

  async mounted() {
    await this.fetchBooks();
    this.filterBooks()
    await this.fetchAuthors()
  }

  get sortedFilteredBooks() {
    return this.filteredBooks.sort((a, b) => {
      const key = this.sortBy;
      if (this.sortDesc) {
        return a[key] > b[key] ? -1 : 1;
      } else {
        return a[key] < b[key] ? -1 : 1;
      }
    });
  }
  
  async fetchBooks() {
    try {
      const accessToken: string | null = getAccessToken();
      if (!accessToken) {
        await this.$router.push('/login');
      }
      this.accessToken = accessToken!
      const response = await this.$axios.get('/book/', {
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      });
      console.log(response.data);
      this.books = response.data.books
    } catch (error: any) {
      if (error.response && error.response.status === 401) {
        await this.$router.push('/login');
      }else{
        console.error(error);
      }
    }
  }

  async fetchAuthors(): Promise<void> {
    try {
      const response = await this.$axios.get('/author', {
        headers: {
          Authorization: `Bearer ${this.accessToken}`,
        },
      });
      this.authors = response.data.authors
    } catch (error: any) {
      if (error.response && error.response.status === 401) {
        await this.$router.push('/login');
      }else{
        console.error(error);
      }
    }
  }

  filterBooks() {
    this.filteredBooks = this.books.filter(book =>
      book.title.toLowerCase().includes(this.searchText.toLowerCase())
    );
  }

  get authorOptions() {
    return this.authors.map((author) => ({
      id: author.id,
      label: author.name,
    }));
  }

  showAddBookModal() {
    this.bookForm = {
      title: '',
      author_id: null,
      pages: 0,
      book_id: null,
      editForm: false,
    };
    this.showBookModal = true;
  }

  hideBookModal() {
    this.showBookModal = false;
  }

  async saveBook() {
    if (this.bookForm.editForm){
      await this.$axios.put(`/book/${this.bookForm.book_id}`, this.bookForm, {
        headers: {
          Authorization: `Bearer ${this.accessToken}`,
        }
      });
    }else{
      await this.$axios.post(`/book`, this.bookForm, {
        headers: {
          Authorization: `Bearer ${this.accessToken}`,
        }
      });
    }
    await this.fetchBooks();
    this.filterBooks()
    this.showBookModal = false;
  }

  editBook(book: any) {
    this.bookForm = {
      title: book.title,
      author_id: book.author.id,
      pages: book.pages,
      book_id: book.id,
      editForm: true
    };
    this.showBookModal = true;
  }
}
</script>
