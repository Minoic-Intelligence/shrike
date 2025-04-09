/*
 * Copyright (c) 2008, Willow Garage, Inc.
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are met:
 *
 *     * Redistributions of source code must retain the above copyright
 *       notice, this list of conditions and the following disclaimer.
 *     * Redistributions in binary form must reproduce the above copyright
 *       notice, this list of conditions and the following disclaimer in the
 *       documentation and/or other materials provided with the distribution.
 *     * Neither the name of Willow Garage, Inc. nor the names of its
 *       contributors may be used to endorse or promote products derived from
 *       this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
 * LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 * CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
 * SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
 * INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
 * CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 * ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 * POSSIBILITY OF SUCH DAMAGE.
 */

/* Author: Brian Gerkey */

#include <stdexcept> // for std::runtime_error
#include <string>
#include <vector>
#include <stdlib.h>
#ifndef _WIN32
#include <unistd.h>
#endif
#include <stdio.h>
#include <time.h>
#include <gtest/gtest.h>
#include <boost/algorithm/string.hpp>
#include <boost/filesystem.hpp>
#include "rospack/rospack.h"
#include "utils.h"

#ifdef _WIN32
int setenv(const char *name, const char *value, int overwrite)
{
  if(!overwrite)
  {
    size_t envsize = 0;
    errno_t errcode = getenv_s(&envsize, NULL, 0, name);
    if(errcode || envsize)
      return errcode;
  }
  return _putenv_s(name, value);
}
#endif

TEST(rospack, reentrant)
{
  rospack::ROSPack rp;
  std::string output;
  int ret = rp.run(std::string("plugins --attrib=foo --top=precedence1 roslang"));
  ASSERT_EQ(ret, 0);
  ret = rp.run(std::string("find roslang"));
  ASSERT_EQ(ret, 0);
  ret = rp.run(std::string("list-names"));
  ASSERT_EQ(ret, 0);
  std::vector<std::string> output_list;
  output = rp.getOutput();
  boost::trim(output);
  boost::split(output_list, output, boost::is_any_of("\n"));
  ASSERT_EQ((int)output_list.size(), 4);
  ret = rp.run(std::string("list"));
  ASSERT_EQ(ret, 0);
  output = rp.getOutput();
  boost::trim(output);
  boost::split(output_list, output, boost::is_any_of("\n"));
  ASSERT_EQ((int)output_list.size(), 4);
  std::vector<std::string> path_name;
  boost::split(path_name, output_list[0], boost::is_any_of(" "));
  ASSERT_EQ((int)path_name.size(), 2);
}

TEST(rospack, multiple_rospack_objects)
{
  rospack::ROSPack rp;
  std::string output;
  int ret = rp.run(std::string("plugins --attrib=foo --top=precedence1 roslang"));
  ASSERT_EQ(ret, 0);
  ret = rp.run(std::string("find roslang"));
  ASSERT_EQ(ret, 0);
  ret = rp.run(std::string("list-names"));
  ASSERT_EQ(ret, 0);
  std::vector<std::string> output_list;
  output = rp.getOutput();
  boost::trim(output);
  boost::split(output_list, output, boost::is_any_of("\n"));
  ASSERT_EQ((int)output_list.size(), 4);
  ret = rp.run(std::string("list"));
  ASSERT_EQ(ret, 0);
  output = rp.getOutput();
  boost::trim(output);
  boost::split(output_list, output, boost::is_any_of("\n"));
  ASSERT_EQ((int)output_list.size(), 4);
  std::vector<std::string> path_name;
  boost::split(path_name, output_list[0], boost::is_any_of(" "));
  ASSERT_EQ((int)path_name.size(), 2);

  rospack::ROSPack rp2;
  ret = rp2.run(std::string("plugins --attrib=foo --top=precedence1 roslang"));
  ASSERT_EQ(ret, 0);
  ret = rp2.run(std::string("find roslang"));
  ASSERT_EQ(ret, 0);
  ret = rp2.run(std::string("list-names"));
  ASSERT_EQ(ret, 0);
  output_list.clear();
  output = rp2.getOutput();
  boost::trim(output);
  boost::split(output_list, output, boost::is_any_of("\n"));
  ASSERT_EQ((int)output_list.size(), 4);
  ret = rp2.run(std::string("list"));
  ASSERT_EQ(ret, 0);
  output = rp2.getOutput();
  boost::trim(output);
  boost::split(output_list, output, boost::is_any_of("\n"));
  ASSERT_EQ((int)output_list.size(), 4);
  path_name.clear();
  boost::split(path_name, output_list[0], boost::is_any_of(" "));
  ASSERT_EQ((int)path_name.size(), 2);
}

TEST(rospack, deduplicate_tokens)
{
  std::string input = "foo foo bar bat bar foobar batbar";
  std::string truth = "foo bar bat foobar batbar";
  std::string output;
  rospack::deduplicate_tokens(input, false, output);
  ASSERT_EQ(truth, output);
}

// Test that env var changes between runs still produce the right results.
TEST(rospack, env_change)
{
  // Get old path for resetting later, to avoid cross-talk with other tests
  char* oldrpp = getenv("ROS_PACKAGE_PATH");
  rospack::ROSPack rp;

  // Case 1: RPP=/test2
  char buf[1024];
  std::string rr = std::string(getcwd(buf, sizeof(buf))) + "/test2";
  setenv("ROS_PACKAGE_PATH", rr.c_str(), 1);
  std::vector<std::string> test_pkgs;
  test_pkgs.push_back("precedence1");
  test_pkgs.push_back("precedence2");
  test_pkgs.push_back("precedence3");
  test_pkgs.push_back("roslang");
  std::string output;
  int ret = rp.run(std::string("list-names"));
  EXPECT_EQ(ret, 0);
  std::vector<std::string> output_list;
  output = rp.getOutput();
  boost::trim(output);
  boost::split(output_list, output, boost::is_any_of("\n"));
  // Check that we get back the right list of packages (which could be in any
  // order).
  EXPECT_EQ(output_list.size(), test_pkgs.size());
  for(std::vector<std::string>::const_iterator it = output_list.begin();
      it != output_list.end();
      ++it)
  {
    bool found = false;
    for(std::vector<std::string>::const_iterator it2 = test_pkgs.begin();
        it2 != test_pkgs.end();
        ++it2)
    {
      if(*it == *it2)
      {
        EXPECT_FALSE(found);
        found = true;
      }
    }
    EXPECT_TRUE(found);
  }

  // Case 2: RPP=/test3
  rr = std::string(getcwd(buf, sizeof(buf))) + "/test3";
  setenv("ROS_PACKAGE_PATH", rr.c_str(), 1);
  test_pkgs.clear();
  test_pkgs.push_back("precedence1");
  test_pkgs.push_back("precedence2");
  test_pkgs.push_back("precedence3");
  ret = rp.run(std::string("list-names"));
  EXPECT_EQ(ret, 0);
  output_list.clear();
  output = rp.getOutput();
  boost::trim(output);
  boost::split(output_list, output, boost::is_any_of("\n"));
  // Check that we get back the right list of packages (which could be in any
  // order).
  EXPECT_EQ(output_list.size(), test_pkgs.size());
  for(std::vector<std::string>::const_iterator it = output_list.begin();
      it != output_list.end();
      ++it)
  {
    bool found = false;
    for(std::vector<std::string>::const_iterator it2 = test_pkgs.begin();
        it2 != test_pkgs.end();
        ++it2)
    {
      if(*it == *it2)
      {
        EXPECT_FALSE(found);
        found = true;
      }
    }
    EXPECT_TRUE(found);
  }

  // Case 3: RPP=/test_empty
  rr = std::string(getcwd(buf, sizeof(buf))) + "/test_empty";
  setenv("ROS_PACKAGE_PATH", rr.c_str(), 1);
  ret = rp.run(std::string("list-names"));
  EXPECT_EQ(ret, 0);
  output = rp.getOutput();
  boost::trim(output);
  EXPECT_EQ(output, std::string());

  // Reset old path, for other tests
  setenv("ROS_PACKAGE_PATH", oldrpp, 1);
}


namespace
{
void trimAll(std::vector<std::string> &inout)
{
  for (ssize_t i = inout.size() - 1; i >= 0; --i)
  {
    boost::trim(inout[i]);
    // Remove empty ones
    if (inout[i].empty()) inout.erase(inout.begin() + i);
  }
}

::testing::AssertionResult outputEqual(std::string output, const std::string &expected, bool trim = true)
{
  if (trim) boost::trim(output);
  if (output == expected) return ::testing::AssertionSuccess();
  return ::testing::AssertionFailure() << "Output did not match: " <<  output;
}

::testing::AssertionResult outputEqual(std::string output, const std::vector<std::string> &expected, bool trim = true)
{
  boost::trim(output);
  std::vector<std::string> output_lines;
  boost::split( output_lines, output, []( char c) { return c == '\n'; });
  if (trim) trimAll( output_lines);
  if ( output_lines.size() != expected.size())
    return ::testing::AssertionFailure() << "output line count did not match expected: " << output_lines.size() << std::endl << boost::join( output_lines, "\n");
  for ( size_t i = 0; i < output_lines.size(); ++i)
  {
    for ( size_t j = i + 1; j < output_lines.size(); ++j)
    {
      if ( output_lines[i] == output_lines[j])
        return ::testing::AssertionFailure() << "output contained a duplicate: " << output_lines[i];
    }
  }
  for (auto &dep : output_lines)
  {
    bool found = false;
    for (auto &line : expected)
    {
      if (line != dep) continue;
      found = true;
      break;
    }
    if (!found)
      return ::testing::AssertionFailure() << "output contained '" << dep << "' which was not expected!";
  }
  return ::testing::AssertionSuccess();
}

::testing::AssertionResult outputEndsWith(std::string output, const std::vector<std::string> &expected, bool trim = true)
{
  boost::trim(output);
  std::vector<std::string> output_lines;
  boost::split( output_lines, output, []( char c) { return c == '\n' || c == ' '; });
  if (trim) trimAll( output_lines);
  if (output_lines.size() != expected.size())
    return ::testing::AssertionFailure() << "output line count did not match expected: " << output_lines.size() << std::endl << boost::join( output_lines, "\n");
  for (size_t i = 0; i < output_lines.size(); ++i)
  {
    for (size_t j = i + 1; j < output_lines.size(); ++j)
    {
      if (output_lines[i] == output_lines[j])
        return ::testing::AssertionFailure() << "output contained a duplicate: " << output_lines[i];
    }
  }
  for (auto &dep : output_lines)
  {
    bool found = false;
    for (auto &line : expected)
    {
      if (dep.length() < line.length()) continue;
      if (line != dep.substr(dep.length() - line.length())) continue;
      found = true;
      break;
    }
    if (!found)
      return ::testing::AssertionFailure() << "output contained '" << dep << "' which was not expected!";
  }
  return ::testing::AssertionSuccess();
}
}

TEST(rospack, multiple_errors)
{
  // Get old path for resetting later, to avoid cross-talk with other tests
  char* oldrpp = getenv("ROS_PACKAGE_PATH");
  // Switch to RPP=/test_errors
  char buf[1024];
  std::string rr = std::string(getcwd(buf, sizeof(buf))) + "/test_errors";
  setenv("ROS_PACKAGE_PATH", rr.c_str(), 1);
  rospack::ROSPack rp;
  std::string output;
  int ret = rp.run("deps valid_package");
  EXPECT_EQ(ret, 0);
  EXPECT_TRUE(outputEqual(rp.getOutput(), std::vector<std::string> {"base", "base2"}));

  // one error
  ret = rp.run("deps invalid_package_one");
  EXPECT_NE(ret, 0);
  EXPECT_TRUE(outputEqual(rp.getOutput(), std::vector<std::string> {"valid_package", "base", "base2"} ));

  // two errors
  ret = rp.run("deps invalid_package_two");
  EXPECT_NE(ret, 0);
  EXPECT_TRUE(outputEqual(rp.getOutput(), {"invalid_package_one", "valid_package", "base", "base2", "another_valid_package"}));

  // depends1
  ret = rp.run("depends1 direct_deps_valid");
  EXPECT_NE(ret, 0);
  EXPECT_TRUE(outputEqual(rp.getOutput(), std::vector<std::string> {"valid_package", "invalid_package_one"}));

  // depends-manifests
  ret = rp.run("depends-manifests invalid_package_one");
  EXPECT_NE(ret, 0);
  EXPECT_TRUE(outputEndsWith(rp.getOutput(), std::vector<std::string> {"valid_package/manifest.xml", "base/manifest.xml", "base2/manifest.xml"}));

  // depends-indent
  ret = rp.run("depends-indent invalid_package_one");
  EXPECT_NE(ret, 0);
  EXPECT_TRUE(outputEqual(rp.getOutput(), std::vector<std::string> {"valid_package", "  base", "  base2"}, false));

  // depends-why
  ret = rp.run("depends-why --target=base invalid_package_two");
  EXPECT_NE(ret, 0);
  EXPECT_TRUE(outputEqual(rp.getOutput(), std::vector<std::string> {"Dependency chains from invalid_package_two to base:",
                                                                    "* invalid_package_two -> invalid_package_one -> valid_package -> base"}));

  // depends-on
  ret = rp.run("depends-on base");
  EXPECT_EQ(ret, 0);
  EXPECT_TRUE(outputEqual(rp.getOutput(), {"direct_deps_valid", "valid_package", "invalid_package_one", "invalid_package_two", "invalid_roslang_package"}));

  // depends-on1
  ret = rp.run("depends-on1 base");
  EXPECT_EQ(ret, 0);
  EXPECT_TRUE(outputEqual(rp.getOutput(), "valid_package"));

  ret = rp.run("depends-on1 valid_package");
  EXPECT_EQ(ret, 0);
  EXPECT_TRUE(outputEqual(rp.getOutput(), std::vector<std::string> {"direct_deps_valid", "invalid_package_one"}));

  // Reset old path, for other tests
  setenv("ROS_PACKAGE_PATH", oldrpp, 1);
}

int main(int argc, char **argv)
{
  // Quiet some warnings
  (void)rospack::ROSPACK_NAME;
  (void)rospack::ROSSTACK_NAME;

  char buf[1024];
  std::string rr = std::string(getcwd(buf, sizeof(buf))) + "/test2";
  setenv("ROS_PACKAGE_PATH", rr.c_str(), 1);
  char *path = getcwd(NULL, 0);
  if(path)
  {
    boost::filesystem::path p(path);
    p = p.parent_path();
    std::string newpath = p.string();
    char* oldpath = getenv("PATH");
    if(oldpath)
      newpath += std::string(":") + oldpath;
    setenv("PATH", newpath.c_str(), 1);
  }

  free(path);
  testing::InitGoogleTest(&argc, argv);
  return RUN_ALL_TESTS();
}
