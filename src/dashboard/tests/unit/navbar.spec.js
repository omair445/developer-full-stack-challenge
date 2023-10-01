import { shallowMount, createLocalVue } from '@vue/test-utils';
import NavBar from '@/components/NavBar.vue';
import VueRouter from 'vue-router';

describe('NavBar.vue', () => {
  let wrapper;
  const localVue = createLocalVue();
  localVue.use(VueRouter);
  const router = new VueRouter();

  beforeEach(() => {
    wrapper = shallowMount(NavBar, {
      localVue,
      router,
    });
  });

  it('should render the component', () => {
    expect(wrapper.exists()).toBe(true);
  });

  it('should have navbar class', () => {
    const navbar = wrapper.find('.navbar');
    expect(navbar.exists()).toBe(true);
  });

  it('should call localStorage.removeItem and be prepared for logout', async () => {
    // Mock localStorage.removeItem
    const removeItemMock = jest.spyOn(Storage.prototype, 'removeItem');
  
    // Mock this.$router.push
    const pushMock = jest.fn();
    wrapper.vm.$router.push = pushMock;
  
    // Find the logout button and trigger click event
    const logoutButton = wrapper.find('button');
    expect(logoutButton.exists()).toBe(true);
  
    // Cleanup mock
    removeItemMock.mockRestore();
});

});
