<template>
  <div>
    <nav-bar></nav-bar>
    <Container>
      <div>
        <b-card title="Authors">
          <div class="mb-3">
            <b-form-input v-model="searchText" placeholder="Search authors" @input="filterAuthors"></b-form-input>
            <b-button @click="showAddModal" variant="success" class="mt-3">Add New Author</b-button>
          </div>
          <b-table
            striped
            hover
            :items="sortedFilteredAuthors"
            :fields="tableFields"
            :current-page="currentPage"
            :per-page="perPage"
            :sort-by.sync="sortBy"
            :sort-desc.sync="sortDesc"
          >
            <template #cell(actions)="row">
              <b-button @click="editAuthor(row.item)" variant="primary" size="sm">Edit</b-button>
            </template>
          </b-table>
          <b-pagination v-model="currentPage" :total-rows="filteredAuthors.length" :per-page="perPage" class="mt-3"></b-pagination>
        </b-card>

        <!-- Add Author Modal -->
        <b-modal hide-footer v-model="addModal" title="Add Author">
          <b-form @submit.prevent="addAuthor">
            <b-form-group label="Name">
              <b-form-input v-model="newAuthor.name" required></b-form-input>
            </b-form-group>
            <b-button type="submit" variant="primary">Save</b-button>
            <b-button @click="hideAddModal" variant="secondary">Cancel</b-button>
          </b-form>
        </b-modal>

        <!-- Add Book Modal -->
        <b-modal hide-footer v-model="addBookModal" title="Add Book">
          <b-form @submit.prevent="addBook">
            <b-form-group label="Title">
              <b-form-input v-model="newBook.title" required></b-form-input>
            </b-form-group>
            <b-form-group label="Number of Pages">
              <b-form-input v-model="newBook.pages" required></b-form-input>
            </b-form-group>
            <b-button type="submit" variant="primary">Save</b-button>
            <b-button @click="hideAddBookModal" variant="secondary">Cancel</b-button>
          </b-form>
        </b-modal>

        <!-- Edit Author Modal -->
        <b-modal hide-footer v-if="editModal" v-model="editModal" title="Edit Author">
          <b-form @submit.prevent="updateAuthor">
            <b-form-group label="Name">
              <b-form-input v-model="selectedAuthor.name" required></b-form-input>
            </b-form-group>
            <b-button type="submit" variant="primary">Save</b-button>
            <b-button @click="hideEditModal" variant="secondary">Cancel</b-button>
          </b-form>
          <b-card title="Books" class="mt-3">
            <b-table striped hover :items="selectedAuthor.books" :fields="bookTableFields">
              <template #cell(actions)="row">
                <b-button @click="editBook(row.item)" variant="primary" size="sm">Edit</b-button>
                <b-button @click="deleteBook(row.item)" variant="danger" size="sm">Delete</b-button>
              </template>
            </b-table>
            <b-button @click="showAddBookModal" variant="success" class="mt-3">Add New Book</b-button>
          </b-card>
        </b-modal>

        <!-- Edit Book Modal -->
        <b-modal hide-footer v-if="editBookModal" v-model="editBookModal" title="Edit Book">
          <b-form @submit.prevent="updateBook">
            <b-form-group label="Book Title">
              <b-form-input v-model="selectedBook.title" required></b-form-input>
            </b-form-group>
            <b-form-group label="Number of Pages">
              <b-form-input v-model="selectedBook.pages" required></b-form-input>
            </b-form-group>
            <b-button type="submit" variant="primary">Save</b-button>
            <b-button @click="hideEditBookModal" variant="secondary">Cancel</b-button>
          </b-form>
        </b-modal>
      </div>
    </Container>
  </div>
</template>

<script lang="ts">

import { Vue, Component } from 'nuxt-property-decorator';
import { getAccessToken } from "../utils/localStorageHelper";

@Component({})
export default class Authors extends Vue {
  private searchText: string = '';
  private authors: any[] = [];
  private filteredAuthors: any[] = [];
  private addModal: boolean = false;
  private editModal: boolean = false;
  private selectedAuthor: any = null;
  private accessToken: string = '';
  private newAuthor: any = {
    name: ''
  };
  private currentPage: number = 1;
  private perPage: number = 7;
  private sortBy: string = 'name'; // The initial column to sort by
  private sortDesc: boolean = true; // true for descending order, false for ascending order

  private tableFields: any[] = [
    { key: 'id', label: 'ID', sortable: true },
    { key: 'name', label: 'Name', sortable: true },
    { key: 'num_books', label: 'Number of Books', sortable: true },
    { key: 'actions', label: 'Actions' },
  ];


  private addBookModal: boolean = false;
  private editBookModal: boolean = false;
  private selectedBook: any = null;
  private newBook: any = {
    title: '',
    pages: 0,
  };

  private bookTableFields: any[] = [
    { key: 'title', label: 'Book Title' },
    { key: 'pages', label: 'Number of Pages' },
    { key: 'actions', label: 'Actions' },
  ];

  async mounted(): Promise<void> {
    await this.fetchAuthors();
  }

  async fetchAuthors(): Promise<void> {
    try {
      const accessToken: string | null = getAccessToken();
      if (!accessToken) {
        await this.$router.push('/login');
      }
      this.accessToken = accessToken!;
      const response = await this.$axios.get('/author/', {
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      });
      this.authors = response.data.authors;
      this.filteredAuthors = response.data.authors;
    } catch (error: any) {
      if (error.response && error.response.status === 401) {
        await this.$router.push('/login');
      } else {
        console.error(error);
      }
    }
  }

  get sortedFilteredAuthors() {
    return this.filteredAuthors.sort((a, b) => {
      const key = this.sortBy;
      if (this.sortDesc) {
        return a[key] > b[key] ? -1 : 1;
      } else {
        return a[key] < b[key] ? -1 : 1;
      }
    });
  }

  filterAuthors(): void {
    this.filteredAuthors = this.authors.filter((author) =>
      author.name.toLowerCase().includes(this.searchText.toLowerCase())
    );
  }

  showAddModal(): void {
    this.addModal = true;
  }

  hideAddModal(): void {
    this.addModal = false;
  }

  editAuthor(author: any): void {
    this.selectedAuthor = { ...author };
    this.editModal = true;
  }

  hideEditModal(): void {
    this.selectedAuthor = null;
    this.editModal = false;
  }

  async addAuthor(): Promise<void> {
    await this.$axios.post('/author', this.newAuthor, {
      headers: {
        Authorization: `Bearer ${this.accessToken}`,
      },
    });
    await this.fetchAuthors();
    this.newAuthor = {
      name: '',
    };
    this.hideAddModal();
  }

  async updateAuthor(): Promise<void> {
    await this.$axios.put(`/author/${this.selectedAuthor.id}`, { name: this.selectedAuthor.name }, {
      headers: {
        Authorization: `Bearer ${this.accessToken}`,
      },
    });
    await this.fetchAuthors();
    this.hideEditModal();
  }

  showAddBookModal(): void {
    this.addBookModal = true;
  }

  hideAddBookModal(): void {
    this.addBookModal = false;
  }

  editBook(book: any): void {
    this.selectedBook = { ...book };
    this.editBookModal = true;
  }

  hideEditBookModal(): void {
    this.selectedBook = null;
    this.editBookModal = false;
  }

  async addBook(): Promise<void> {
    await this.$axios.post(`/book`, { ...this.newBook, author_id: this.selectedAuthor.id }, {
      headers: {
        Authorization: `Bearer ${this.accessToken}`,
      },
    });
    await this.fetchAuthors();
    this.newBook = {
      title: '',
      pages: 0,
    };
    this.hideAddBookModal();
    this.hideEditModal();
  }

  async updateBook(): Promise<void> {
    await this.$axios.put(`/book/${this.selectedBook.id}`, this.selectedBook, {
      headers: {
        Authorization: `Bearer ${this.accessToken}`,
      },
    });
    await this.fetchAuthors();
    this.hideEditBookModal();
    this.hideEditModal();
  }

  async deleteBook(book: any): Promise<void> {
    if (confirm("Are you sure you want to delete this book?")) {
      await this.$axios.delete(`/book/${book.id}`, {
        headers: {
          Authorization: `Bearer ${this.accessToken}`,
        },
      });
      await this.fetchAuthors();
      this.hideEditBookModal();
      this.hideEditModal();
    }
  }

}
</script>
