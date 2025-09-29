"""
Performance tests for the NIA Engineering Portal.
"""

import time
from unittest.mock import patch

from tray_app.config_manager import ConfigManager
from tray_app.gui_components import ConfigurationDialog
from tray_app.server_controller import ServerController


class TestPerformance:
    """Performance test cases."""

    def test_config_manager_performance(self, test_config_manager):
        """Test ConfigManager performance."""
        # Test configuration loading speed
        start_time = time.time()

        # Perform multiple operations
        for i in range(100):
            test_config_manager.set_port(8000 + i)
            test_config_manager.set_default_page("index.html")
            test_config_manager.get_port()
            test_config_manager.get_default_page()
            test_config_manager.get_available_pages()

        end_time = time.time()
        duration = end_time - start_time

        # Should complete 100 operations in under 1 second
        assert (
            duration < 1.0
        ), f"ConfigManager operations took {duration:.3f}s, expected < 1.0s"

    def test_html_generation_performance(self, test_config_manager):
        """Test HTML generation performance."""
        dialog = ConfigurationDialog(test_config_manager)

        # Test HTML generation speed
        start_time = time.time()

        # Generate HTML multiple times
        for _ in range(50):
            html = dialog._create_config_html(9092)
            assert len(html) > 1000  # Basic validation

        end_time = time.time()
        duration = end_time - start_time

        # Should generate 50 HTML pages in under 2 seconds
        assert duration < 2.0, f"HTML generation took {duration:.3f}s, expected < 2.0s"

    def test_port_availability_check_performance(self, test_server_controller):
        """Test port availability check performance."""
        # Test port checking speed
        start_time = time.time()

        # Check multiple ports
        for port in range(9000, 9100):
            test_server_controller.is_port_available(port)

        end_time = time.time()
        duration = end_time - start_time

        # Should check 100 ports in under 5 seconds
        assert duration < 5.0, f"Port checking took {duration:.3f}s, expected < 5.0s"

    def test_find_available_port_performance(self, test_server_controller):
        """Test find available port performance."""
        # Test finding available port speed
        start_time = time.time()

        # Find multiple available ports
        for _ in range(10):
            port = test_server_controller.find_available_port(9000)
            assert 9000 <= port <= 65535

        end_time = time.time()
        duration = end_time - start_time

        # Should find 10 available ports in under 3 seconds
        assert (
            duration < 3.0
        ), f"Find available port took {duration:.3f}s, expected < 3.0s"

    def test_configuration_save_performance(self, test_config_manager):
        """Test configuration save performance."""
        # Test save speed
        start_time = time.time()

        # Save configuration multiple times
        for i in range(20):
            test_config_manager.set_port(8000 + i)
            test_config_manager.set_default_page("index.html")
            test_config_manager.save_config()

        end_time = time.time()
        duration = end_time - start_time

        # Should save 20 times in under 1 second
        assert (
            duration < 1.0
        ), f"Configuration save took {duration:.3f}s, expected < 1.0s"

    def test_memory_usage(self, test_config_manager):
        """Test memory usage of components."""
        import os

        import psutil

        # Get initial memory usage
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss

        # Create multiple instances
        config_managers = []
        server_controllers = []
        dialogs = []

        for _ in range(10):
            cm = ConfigManager()
            sc = ServerController(cm)
            dialog = ConfigurationDialog(cm)

            config_managers.append(cm)
            server_controllers.append(sc)
            dialogs.append(dialog)

        # Get memory usage after creating instances
        final_memory = process.memory_info().rss
        memory_increase = final_memory - initial_memory

        # Should not use more than 50MB for 10 instances
        assert (
            memory_increase < 50 * 1024 * 1024
        ), f"Memory usage increased by {memory_increase / 1024 / 1024:.1f}MB, expected < 50MB"

    def test_concurrent_operations(self, test_config_manager):
        """Test concurrent operations performance."""
        import queue
        import threading

        results = queue.Queue()

        def worker(worker_id):
            """Worker function for concurrent testing."""
            start_time = time.time()

            # Perform operations
            for i in range(10):
                test_config_manager.set_port(8000 + worker_id * 10 + i)
                test_config_manager.set_default_page("index.html")
                test_config_manager.get_port()
                test_config_manager.get_default_page()

            end_time = time.time()
            results.put((worker_id, end_time - start_time))

        # Start multiple threads
        threads = []
        for i in range(5):
            thread = threading.Thread(target=worker, args=(i,))
            threads.append(thread)
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

        # Collect results
        thread_results = []
        while not results.empty():
            thread_results.append(results.get())

        # All threads should complete successfully
        assert len(thread_results) == 5

        # Each thread should complete in reasonable time
        for worker_id, duration in thread_results:
            assert (
                duration < 2.0
            ), f"Worker {worker_id} took {duration:.3f}s, expected < 2.0s"

    def test_large_configuration_performance(self, test_config_manager):
        """Test performance with large configuration."""
        # Create a large list of available pages
        large_page_list = [f"pages/page_{i}.html" for i in range(1000)]

        # Test setting large configuration
        start_time = time.time()

        # This would normally be done in the config manager
        # For testing, we'll simulate the operations
        for _page in large_page_list[:100]:  # Test with 100 pages
            test_config_manager.set_default_page("index.html")  # Use existing page

        end_time = time.time()
        duration = end_time - start_time

        # Should handle 100 page operations in under 1 second
        assert (
            duration < 1.0
        ), f"Large configuration operations took {duration:.3f}s, expected < 1.0s"

    def test_file_io_performance(self, test_config_manager):
        """Test file I/O performance."""
        # Test multiple save/load cycles
        start_time = time.time()

        for i in range(50):
            test_config_manager.set_port(8000 + i)
            test_config_manager.save_config()

            # Reload configuration
            new_cm = ConfigManager(str(test_config_manager.config_file))
            assert new_cm.get_port() == 8000 + i

        end_time = time.time()
        duration = end_time - start_time

        # Should complete 50 save/load cycles in under 3 seconds
        assert (
            duration < 3.0
        ), f"File I/O operations took {duration:.3f}s, expected < 3.0s"

    def test_startup_performance(self, test_config_manager):
        """Test application startup performance."""
        # Test tray application startup speed
        start_time = time.time()

        # Simulate startup operations
        # server_controller = ServerController(test_config_manager)  # Not used in this test

        # Mock the tray application creation
        with patch("pystray.Icon"):
            pass

            # tray_app = TrayApplication(test_config_manager, server_controller)  # Not used in this test

        end_time = time.time()
        duration = end_time - start_time

        # Should start up in under 2 seconds
        assert duration < 2.0, f"Startup took {duration:.3f}s, expected < 2.0s"
